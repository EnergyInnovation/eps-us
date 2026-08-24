# RunEPS.ps1 - launch a Vensim .cmd headless and watch for blocking dialogs.
#
# Vensim pops modal dialogs that a hidden batch run cannot answer, and a model
# error writes NOTHING useful to vensimdp.err - the run just hangs forever.
# This wrapper polls for those dialogs, answers the benign ones, and for a model
# error it clicks through to the equation editor and reads out the real error
# text and the offending variable, then stops the run.
#
# Usage:  .\RunEPS.ps1 -Cmd MyRun.cmd [-Expect MyRun.tab] [-TimeoutMinutes 10]
# Exit:   0 = finished, 2 = model error (details printed), 3 = timeout

param(
    [Parameter(Mandatory=$true)][string]$Cmd,
    [string]$Expect = "",
    [int]$TimeoutMinutes = 10,
    [string]$Vendss = "C:\Program Files\Vensim\vendss64.exe"
)

Add-Type -TypeDefinition @'
using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Text;
public class VenWatch {
    public delegate bool EnumProc(IntPtr hWnd, IntPtr lParam);
    [DllImport("user32.dll")] public static extern bool EnumWindows(EnumProc cb, IntPtr lParam);
    [DllImport("user32.dll")] public static extern bool EnumChildWindows(IntPtr h, EnumProc cb, IntPtr lParam);
    [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);
    [DllImport("user32.dll", CharSet=CharSet.Auto)] public static extern int GetClassName(IntPtr h, StringBuilder sb, int max);
    [DllImport("user32.dll", CharSet=CharSet.Auto)] public static extern int GetWindowText(IntPtr h, StringBuilder sb, int max);
    [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
    [DllImport("user32.dll")] public static extern IntPtr SendMessage(IntPtr h, uint msg, IntPtr wp, IntPtr lp);
    [DllImport("user32.dll", CharSet=CharSet.Auto, EntryPoint="SendMessage")] public static extern IntPtr SendMessageText(IntPtr h, uint msg, IntPtr wp, StringBuilder lp);
    const uint BM_CLICK = 0x00F5;
    const uint WM_GETTEXT = 0x000D;
    const uint WM_GETTEXTLENGTH = 0x000E;

    // every visible top-level window of this pid, as "class|title|handle"
    public static List<string> Windows(int pid) {
        var res = new List<string>();
        EnumWindows((h, lp) => {
            uint wpid; GetWindowThreadProcessId(h, out wpid);
            if (wpid == (uint)pid && IsWindowVisible(h)) {
                var c = new StringBuilder(256); GetClassName(h, c, 256);
                var t = new StringBuilder(1024); GetWindowText(h, t, 1024);
                res.Add(c.ToString() + "|" + t.ToString() + "|" + h.ToInt64());
            }
            return true;
        }, IntPtr.Zero);
        return res;
    }
    // all child control texts of a window, as "class::text"
    public static List<string> Children(IntPtr parent) {
        var res = new List<string>();
        EnumChildWindows(parent, (c, lp) => {
            var cls = new StringBuilder(256); GetClassName(c, cls, 256);
            int len = (int)SendMessage(c, WM_GETTEXTLENGTH, IntPtr.Zero, IntPtr.Zero);
            string t = "";
            if (len > 0) { var sb = new StringBuilder(len + 2); SendMessageText(c, WM_GETTEXT, (IntPtr)(len + 2), sb); t = sb.ToString(); }
            res.Add(cls.ToString() + "::" + t);
            return true;
        }, IntPtr.Zero);
        return res;
    }
    public static bool ClickButton(IntPtr dlg, string label) {
        bool clicked = false;
        EnumChildWindows(dlg, (c, lp) => {
            var cls = new StringBuilder(256); GetClassName(c, cls, 256);
            var txt = new StringBuilder(256); GetWindowText(c, txt, 256);
            if (cls.ToString() == "Button" && txt.ToString().Replace("&","").Trim().ToLower() == label.ToLower()) {
                SendMessage(c, BM_CLICK, IntPtr.Zero, IntPtr.Zero); clicked = true; return false;
            }
            return true;
        }, IntPtr.Zero);
        return clicked;
    }
}
'@

$proc = Start-Process -FilePath $Vendss -ArgumentList $Cmd -WorkingDirectory $PWD -PassThru -WindowStyle Hidden
Write-Output "launched pid $($proc.Id) for $Cmd"

$deadline = (Get-Date).AddMinutes($TimeoutMinutes)
$status   = "running"
$errText  = ""
$errVar   = ""

while ((Get-Date) -lt $deadline) {
    Start-Sleep -Seconds 6
    if ($Expect -and (Test-Path $Expect)) { $status = "done"; break }
    if ($proc.HasExited) { $status = "exited"; break }

    $wins = [VenWatch]::Windows($proc.Id)
    $dlg  = $wins | Where-Object { $_ -like "#32770|*" } | Select-Object -First 1
    if (-not $dlg) { continue }

    $h    = [IntPtr][int64]($dlg -split '\|')[2]
    $kids = [VenWatch]::Children($h)
    $body = ($kids | Where-Object { $_ -like "Static::*" } | ForEach-Object { ($_ -split '::',2)[1] }) -join ' '

    if ($body -match "autosave|auto-save|recover") {
        # benign: a stale autosave copy exists; never load it in batch
        [VenWatch]::ClickButton($h, "No") | Out-Null
        Write-Output "dismissed autosave prompt"
        continue
    }

    if ($body -match "errors|cannot be simulated") {
        # model error: click Yes to open the equation editor on the bad variable
        Write-Output "MODEL ERROR dialog: $body"
        [VenWatch]::ClickButton($h, "Yes") | Out-Null
        Start-Sleep -Seconds 3
        foreach ($w in [VenWatch]::Windows($proc.Id)) {
            $parts = $w -split '\|'
            if ($parts[1] -like "Edit:*" -or $parts[0] -eq "#32770") {
                $eh = [IntPtr][int64]$parts[2]
                $ck = [VenWatch]::Children($eh)
                # the message sits in a ComboBox just after the "Errors:" static label
                for ($i = 0; $i -lt $ck.Count; $i++) {
                    if ($ck[$i] -match '^Static::\s*Errors') {
                        for ($j = $i + 1; $j -lt [Math]::Min($i + 4, $ck.Count); $j++) {
                            $t = ($ck[$j] -split '::',2)[1]
                            if ($t -and $t.Trim()) { $errText = $t.Trim(); break }
                        }
                    }
                }
                if ($parts[1] -like "Edit:*") { $errVar = $parts[1] }
                if ($errText) { break }
            }
        }
        $status = "model_error"
        break
    }

    # unknown dialog - report it rather than guessing which button to press
    Write-Output "UNKNOWN dialog: $(($dlg -split '\|')[1]) :: $body"
    $status = "unknown_dialog"
    $errText = $body
    break
}

if (-not $proc.HasExited) { Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue }

switch ($status) {
    "model_error" {
        Write-Output "=== MODEL ERROR ==="
        if ($errVar)  { Write-Output "variable: $errVar" }
        if ($errText) { Write-Output "message : $errText" }
        exit 2
    }
    "unknown_dialog" { Write-Output "=== BLOCKED ON DIALOG ==="; Write-Output $errText; exit 2 }
    "done"   { Write-Output "=== OK (produced $Expect) ==="; exit 0 }
    "exited" { Write-Output "=== process exited; expected file present: $([bool](Test-Path $Expect)) ==="; if ($Expect -and -not (Test-Path $Expect)) { exit 2 } else { exit 0 } }
    default  { Write-Output "=== TIMEOUT after $TimeoutMinutes min ==="; exit 3 }
}
