import mysql.connector
from datetime import datetime
import re


conn = mysql.connector.connect(
    host="localhost",
    user="root",        
    password="password",    
    database="sensors"
)
cursor = conn.cursor()

print("[INFO] Connected to database. Waiting for data...\n")

with open("out_pipe", "r") as pipe:
    while True:
        line = pipe.readline()
        if not line:
            continue

        #  εδώ καθαρίζουμε μη εκτυπώσιμους χαρακτήρες
        line = re.sub(r'[^\x20-\x7E]', '', line).strip()

        # Regex για να βρει ακριβώς ό,τι μας ενδιαφέρει
        match = re.search(
            r"ID=(\d+)\s*\|\s*Count=(\d+)\s*\|\s*Temp=([\d.]+)[°C]*\s*\|\s*Hum=([\d.]+)",
            line
        )

        if match:
            try:
                node_id = int(match.group(1))
                count = int(match.group(2))
                temp = float(match.group(3))
                hum = float(match.group(4))
                timestamp = datetime.now()

                cursor.execute("""
                    INSERT INTO measurements (timestamp, node_id, count, temperature, humidity)
                    VALUES (%s, %s, %s, %s, %s)
                """, (timestamp, node_id, count, temp, hum))

                conn.commit()
                print(f"[DB] Stored | ID={node_id} | Count={count} | Temp={temp}°C | Hum={hum}%")

            except Exception as e:
                print("[ERROR]", e)
        else:
            print("[SKIP]", line)

