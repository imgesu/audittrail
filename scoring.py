import pandas as pd

def risk_score_audit_trail(df):
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    df["Hour"] = df["Timestamp"].dt.hour
    df["DayOfWeek"] = df["Timestamp"].dt.dayofweek
    df["Risk_Flags"] = ""
    df["Risk_Score"] = 0

    for i in range(len(df)):
        row = df.iloc[i]
        flags = []
        score = 0

        if row["Hour"] < 6 or row["Hour"] > 20:
            flags.append("Off-hour activity")
            score += 1

        if row["DayOfWeek"] >= 5:
            flags.append("Weekend activity")
            score += 1

        if row["Action"] == "Approve Record":
            related = df[
                (df["User"] == row["User"]) &
                (df["Action"] == "Create Record") &
                (df["Timestamp"] < row["Timestamp"]) &
                (df["Timestamp"] >= row["Timestamp"] - pd.Timedelta(minutes=30))
            ]
            if not related.empty:
                flags.append("Self-approve within 30min")
                score += 2

        df.at[i, "Risk_Flags"] = ", ".join(flags)
        df.at[i, "Risk_Score"] = score

    return df
