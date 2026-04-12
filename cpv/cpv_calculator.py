import sqlite3
import os
from mock_ad_spend import AD_SPEND_PER_NICHE

def calculate_niche_metrics():
    # Path logic: assumes script is run from within the cpv/ directory
    db_path = os.path.join("..", "data", "classified.db")
    
    if not os.path.exists(db_path):
        print(f"Error: Database not found at {db_path}")
        return []

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Fetch all videos
        cursor.execute("SELECT niche, views FROM videos")
        rows = cursor.fetchall()
    except sqlite3.OperationalError as e:
        print(f"Database Error: {e}")
        return []
    finally:
        conn.close()

    # Dictionary to aggregate data manually
    # Structure: { niche_name: [total_views, total_spend, video_count] }
    stats = {}

    for niche, views in rows:
        # Get mock spend for this niche from our dictionary
        # Default to 0 if niche is not in our list
        spend_per_video = AD_SPEND_PER_NICHE.get(niche, 0)
        
        if niche not in stats:
            stats[niche] = {"views": 0, "spend": 0, "count": 0}
        
        stats[niche]["views"] += views
        stats[niche]["spend"] += spend_per_video
        stats[niche]["count"] += 1

    # Format into the required list of dicts
    results = []
    for niche, data in stats.items():
        total_views = data["views"]
        total_spend = data["spend"]
        
        # Calculate Average CPV (Total Spend / Total Views)
        # Avoid division by zero
        avg_cpv = total_spend / total_views if total_views > 0 else 0
        
        results.append({
            "niche": niche,
            "avg_cpv": round(avg_cpv, 4),
            "total_views": total_views,
            "total_spend": total_spend,
            "video_count": data["count"]
        })

    # Sort by avg_cpv ascending (lowest CPV = Rank 1)
    sorted_results = sorted(results, key=lambda x: x['avg_cpv'])

    return sorted_results

if __name__ == "__main__":
    # Test print for your hackathon demo
    metrics = calculate_niche_metrics()
    print(f"{'Niche':<20} | {'Avg CPV':<10} | {'Views':<10} | {'Count'}")
    print("-" * 55)
    for m in metrics:
        print(f"{m['niche']:<20} | {m['avg_cpv']:<10.4f} | {m['total_views']:<10} | {m['video_count']}")