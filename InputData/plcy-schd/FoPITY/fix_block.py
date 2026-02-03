def fix_block(entries):
    out = []
    pending = {}

    enduse_labels = {
        "boilers",
        "nonboiler low temp",
        "nonboiler med temp",
        "nonboiler high temp",
        "cooling",
        "machine drive",
        "electrochemical",
        "other processes",
    }

    for entry in entries:
        key = entry[0]
        schedules = entry[1:]

        # Try to detect where enduse is
        if len(key) == 3:
            a, b, c = key

            if c in enduse_labels:
                policy, industry, enduse = a, b, c
            elif b in enduse_labels:
                policy, enduse, industry = a, b, c
            else:
                out.append(entry)
                continue
        else:
            out.append(entry)
            continue

        # Remove electrochemical
        if enduse == "electrochemical":
            pending[(policy, industry)] = schedules
            continue

        out.append(entry)

        # Insert after other processes
        if enduse == "other processes":
            k = (policy, industry)
            if k in pending:
                sched = pending.pop(k)

                for new_enduse in (
                    "facility HVAC",
                    "facility lighting",
                    "other nonprocess",
                ):
                    out.append(((policy, industry, new_enduse), *sched))

    return out

entries = fix_block(entries)
