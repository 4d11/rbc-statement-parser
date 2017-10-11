import re
strs = [
    "10 Dec Interac purchase - 0644 KABOB HUT 7.89 1,415.33",
    "14 Dec Interac purchase - 3342 KABOB HUT 7.89",
    "Interac purchase - 6243 SUBWAY # 2969 8.76 1,398.68",
    "15 Dec Interac purchase - 2953 UW BRUBAKERS SL 6.22 1,392.46",
    "23 Dec Online Banking payment - 8933",
    "BELL CANADA 69.87 1,247.28"
]

for s in strs:
    s = s.split()
    if s[-1].isdigit():
        balance = s[-1]
        withdrawals = s[-2]




