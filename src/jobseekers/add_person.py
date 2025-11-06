import psycopg2

def add_person():
    print("\n=== Add Jobseeker ===")
    name = input("Name: ").strip()
    location = input("Location (e.g., Hamilton): ").strip()
    skills = input("Skills (comma separated): ").strip().split(",")
    qualities = input("Personal Qualities (comma separated, optional): ").strip().split(",")
    lived_experience = input("Lived Experience / Story: ").strip()

    skills = [s.strip() for s in skills if s.strip()]
    qualities = [q.strip() for q in qualities if q.strip()]

    conn = psycopg2.connect(
        dbname="ara_mahi",
        user="postgres",
        host="localhost"
    )
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO jobseekers (name, location, skills, qualities, lived_experience)
        VALUES (%s, %s, %s, %s, %s)
    """, (name, location, skills, qualities, lived_experience))
    conn.commit()
    conn.close()

    print("\n Added jobseeker:", name)

if __name__ == "__main__":
    add_person()
