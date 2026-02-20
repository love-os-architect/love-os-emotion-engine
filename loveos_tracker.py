import pandas as pd
import matplotlib.pyplot as plt
import datetime
import os

class LoveOSTracker:
    def __init__(self, csv_file="loveos_log.csv"):
        self.csv_file = csv_file
        # Noise tolerance coefficient (Lock condition: omega <= kappa * R)
        self.kappa = 1.0  
        self.columns = ["Date", "Time", "R", "Omega", "Z_pre", "Z_post", "Delta_Z", "Lock"]
        
        if not os.path.exists(self.csv_file):
            df = pd.DataFrame(columns=self.columns)
            df.to_csv(self.csv_file, index=False)

    def log_entry(self, r, omega, z_pre, z_post):
        """Log daily measurement data."""
        delta_z = z_post - z_pre
        is_locked = omega <= (self.kappa * r)
        
        now = datetime.datetime.now()
        new_data = {
            "Date": now.strftime("%Y-%m-%d"),
            "Time": now.strftime("%H:%M:%S"),
            "R": r,
            "Omega": omega,
            "Z_pre": z_pre,
            "Z_post": z_post,
            "Delta_Z": delta_z,
            "Lock": is_locked
        }
        
        df = pd.read_csv(self.csv_file)
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        df.to_csv(self.csv_file, index=False)
        print(f"Logged: R={r}, Omega={omega}, Lock={is_locked}, Delta_Z={delta_z}")

    def plot_weekly_trends(self):
        """Visualize recent trends and the Lock Rate."""
        df = pd.read_csv(self.csv_file)
        if df.empty:
            print("No data to plot.")
            return

        df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
        # Display the latest 14 logs
        df = df.sort_values('Datetime').tail(14) 

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

        # Top subplot: Trends of R, Omega, Z_pre
        ax1.plot(df['Datetime'], df['R'], marker='o', label='R (Resource)', color='blue')
        ax1.plot(df['Datetime'], df['Omega'], marker='x', label='Omega (Noise)', color='red')
        ax1.plot(df['Datetime'], df['Z_pre'], marker='s', label='Z (Alignment)', color='green')
        ax1.set_ylabel('Level (1-5)')
        ax1.set_title('LoveOS 6D Phase Space Dynamics')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Bottom subplot: Delta Z (Intervention effect) and Lock state
        colors = ['red' if val > 0 else 'blue' for val in df['Delta_Z']]
        ax2.bar(df['Datetime'], df['Delta_Z'], color=colors, alpha=0.6, label='Delta Z (Post-MIRROR)')
        
        # Calculate Lock Rate
        lock_rate = df['Lock'].mean() * 100
        ax2.axhline(0, color='black', linewidth=1)
        ax2.set_ylabel('Delta Z (Target < 0)')
        ax2.set_title(f'MIRROR-30 Efficacy & Lock Rate: {lock_rate:.1f}%')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

# --- Usage Example ---
if __name__ == "__main__":
    tracker = LoveOSTracker()
    
    # Simple UI for entering data from the terminal
    print("--- LoveOS Data Entry ---")
    try:
        r = float(input("Enter R (Resource 1-5): "))
        omega = float(input("Enter Omega (Noise 1-5): "))
        z_pre = float(input("Enter Z pre-MIRROR (1-5): "))
        z_post = float(input("Enter Z post-MIRROR (1-5): "))
        
        tracker.log_entry(r, omega, z_pre, z_post)
        tracker.plot_weekly_trends()
        
    except ValueError:
        print("Input cancelled or invalid. Showing existing plot.")
        tracker.plot_weekly_trends()
