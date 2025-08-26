import argparse, os, hashlib, json
from datetime import datetime, date, timedelta
import pandas as pd

def daterange(start, end):
    cur = start
    while cur <= end:
        yield cur
        cur += timedelta(days=1)

def compute_pdc(claims, start, end, drug_class):
    # Very small illustrative PDC (days covered / days in period)
    df = claims[claims["drug_class"]==drug_class].copy()
    df["fill_date"] = pd.to_datetime(df["fill_date"])
    days = (end - start).days + 1
    # build coverage per member
    cover = {}
    for (m, d, supply) in df[["member_id","fill_date","days_supply"]].itertuples(index=False):
        dates = pd.date_range(d, d + pd.Timedelta(days=supply-1), freq="D")
        cover.setdefault(m, set()).update(set(dates))
    # compute ratio
    rows = []
    for m in df["member_id"].unique().tolist():
        covered = len([x for x in cover.get(m, set()) if start <= x.date() <= end])
        rows.append({"member_id": m, f"pdc_{drug_class}": round(covered / days, 3)})
    return pd.DataFrame(rows)

def compute_supd(claims, start, end):
    # SUPD (demo): diabetes >=2 fills AND >=1 statin fill in the period
    df = claims.copy()
    df["fill_date"] = pd.to_datetime(df["fill_date"])
    df = df[(df["fill_date"].dt.date >= start) & (df["fill_date"].dt.date <= end)]
    agg = df.groupby(["member_id","drug_class"]).size().unstack(fill_value=0)
    supd_flag = ((agg.get("diabetes",0) >= 2) & (agg.get("statin",0) >= 1)).astype(int)
    out = supd_flag.reset_index().rename(columns={0: "supd_flag"})
    return out[["member_id"]].assign(supd_flag=supd_flag.values)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default="2024-01-01")
    ap.add_argument("--end", default="2024-12-31")
    ap.add_argument("--elig", default="data_demo/eligibility.csv")
    ap.add_argument("--rx", default="data_demo/pharmacy_claims.csv")
    args = ap.parse_args()

    start = datetime.strptime(args.start, "%Y-%m-%d").date()
    end = datetime.strptime(args.end, "%Y-%m-%d").date()

    elig = pd.read_csv(args.elig, dtype={"member_id": str})
    rx = pd.read_csv(args.rx, dtype={"member_id": str})

    pdc_d = compute_pdc(rx, start, end, "diabetes")
    pdc_s = compute_pdc(rx, start, end, "statin")
    supd = compute_supd(rx, start, end)

    # Member-level
    member = elig[["member_id","contract_id"]].drop_duplicates()
    member = member.merge(pdc_d, on="member_id", how="left")
    member = member.merge(pdc_s, on="member_id", how="left")
    member = member.merge(supd, on="member_id", how="left").fillna(0)

    os.makedirs("output_demo", exist_ok=True)
    member.to_csv("output_demo/measure_member_results.csv", index=False)

    # Contract rollup (simple demo rollup)
    roll = member.groupby("contract_id").agg(
        members=("member_id","nunique"),
        pdc_diabetes_avg=("pdc_diabetes","mean"),
        pdc_statin_avg=("pdc_statin","mean"),
        supd_rate=("supd_flag","mean"),
    ).reset_index()
    roll.to_csv("output_demo/measure_contract_rollup.csv", index=False)

    # Evidence bundle
    run = {
        "start_date": args.start,
        "end_date": args.end,
        "inputs": {
            "eligibility": args.elig,
            "pharmacy_claims": args.rx,
        },
        "rows": {
            "member_results": len(member),
            "contract_rollup": len(roll),
        },
        "code_hash": hashlib.sha256(open(__file__,"rb").read()).hexdigest()[:16],
        "timestamp": datetime.utcnow().isoformat()+"Z"
    }
    os.makedirs("evidence", exist_ok=True)
    with open(f"evidence/RUN_{date.today().isoformat()}.json","w") as f:
        json.dump(run, f, indent=2)
    print("Wrote output_demo/*.csv and evidence JSON.")

if __name__ == "__main__":
    main()
