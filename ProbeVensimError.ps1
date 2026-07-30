# Dump EVERY child control (class + text, unfiltered) of Vensim's equation-editor
# error dialog, to locate the error message text.
param([string]$Cmd = "MeasRunNew.cmd")
$repo = "C:\Users\DanOBrien\Models\EPS\US\eps-us"
$vendss = "C:\Program Files\Vensim\vendss64.exe"

Add-Type -TypeDefinition @'
using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Text;
public class WinProbe2 {
    public delegate bool EnumProc(IntPtr hWnd, IntPtr lParam);
    [DllImport("user32.dll")] public static extern bool EnumWindows(EnumProc cb, IntPtr lParam);
    [DllImport("user32.dll")] public static extern bool EnumChildWindows(IntPtr h, EnumProc cb, IntPtr lParam);
    [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);
    [DllImport("user32.dll", CharSet=CharSet.Auto)] public static extern int GetClassName(IntPtr h, StringBuilder sb, int max);
    [DllImport("user32.dll", CharSet=CharSet.Auto)] public static extern int GetWindowText(IntPtr h, StringBuilder sb, int max);
    [DllImport("user32.dll")] public static extern IntPtr SendMessage(IntPtr h, uint msg, IntPtr wp, IntPtr lp);
    [DllImport("user32.dll", CharSet=CharSet.Auto, EntryPoint="SendMessage")] public static extern IntPtr SendMessageText(IntPtr h, uint msg, IntPtr wp, StringBuilder lp);
    [DllImport("user32.dll")] public static extern bool ShowWindowAsync(IntPtr h, int nCmdShow);
    [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
    public struct RECT { public int Left, Top, Right, Bottom; }
    const uint BM_CLICK = 0x00F5;
    const uint WM_GETTEXT = 0x000D;
    const uint WM_GETTEXTLENGTH = 0x000E;

    public static IntPtr FindDialog(int pid) {
        IntPtr found = IntPtr.Zero;
        EnumWindows((h, lp) => {
            uint wpid; GetWindowThreadProcessId(h, out wpid);
            if (wpid == (uint)pid) {
                var cls = new StringBuilder(256); GetClassName(h, cls, 256);
                if (cls.ToString() == "#32770") { found = h; return false; }
            }
            return true;
        }, IntPtr.Zero);
        return found;
    }
    public static string TitleOf(IntPtr h) {
        var txt = new StringBuilder(1024); GetWindowText(h, txt, 1024); return txt.ToString();
    }
    public static bool ClickButton(IntPtr dlg, string label) {
        bool clicked = false;
        EnumChildWindows(dlg, (c, lp) => {
            var cls = new StringBuilder(256); GetClassName(c, cls, 256);
            var txt = new StringBuilder(256); GetWindowText(c, txt, 256);
            if (cls.ToString() == "Button" && txt.ToString().Replace("&", "") == label) {
                SendMessage(c, BM_CLICK, IntPtr.Zero, IntPtr.Zero); clicked = true; return false;
            }
            return true;
        }, IntPtr.Zero);
        return clicked;
    }
    public static List<string> DumpChildren(IntPtr parent) {
        var results = new List<string>();
        EnumChildWindows(parent, (c, lp) => {
            var cls = new StringBuilder(256); GetClassName(c, cls, 256);
            int len = (int)SendMessage(c, WM_GETTEXTLENGTH, IntPtr.Zero, IntPtr.Zero);
            string t = "";
            if (len > 0 && len < 20000) {
                var buf = new StringBuilder(len + 1);
                SendMessageText(c, WM_GETTEXT, (IntPtr)(len + 1), buf);
                t = buf.ToString().Replace("\r\n", " / ").Trim();
            }
            RECT r; GetWindowRect(c, out r);
            results.Add("[" + cls + "] y=" + r.Top + " len=" + len + " '" + (t.Length > 900 ? t.Substring(0,900) : t) + "'");
            return true;
        }, IntPtr.Zero);
        return results;
    }
    public static void HideAll(int pid) {
        EnumWindows((h, lp) => {
            uint wpid; GetWindowThreadProcessId(h, out wpid);
            if (wpid == (uint)pid) ShowWindowAsync(h, 0);
            return true;
        }, IntPtr.Zero);
    }
}
'@

$p = Start-Process -FilePath $vendss -ArgumentList $Cmd -WorkingDirectory $repo -PassThru -WindowStyle Hidden
Write-Output "launched PID $($p.Id)"
$dlg = [IntPtr]::Zero
for ($i = 0; $i -lt 120; $i++) {
    Start-Sleep -Seconds 2
    if ($p.HasExited) { Write-Output "exited early"; exit }
    $dlg = [WinProbe2]::FindDialog($p.Id)
    if ($dlg -ne [IntPtr]::Zero) { break }
}
if ($dlg -eq [IntPtr]::Zero) { Write-Output "no dialog"; Stop-Process -Id $p.Id -Force -Confirm:$false; exit }
[void][WinProbe2]::ClickButton($dlg, "Yes")
Start-Sleep -Seconds 8
[WinProbe2]::HideAll($p.Id)
$eq = [WinProbe2]::FindDialog($p.Id)
if ($eq -ne [IntPtr]::Zero) {
    Write-Output ("EQ DIALOG: " + [WinProbe2]::TitleOf($eq))
    [WinProbe2]::DumpChildren($eq) | ForEach-Object { Write-Output $_ }
} else { Write-Output "no equation dialog found" }
Stop-Process -Id $p.Id -Force -Confirm:$false
Write-Output "killed"
