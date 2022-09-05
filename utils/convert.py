def humanizeBytes(B):
    """Return the given bytes as a human friendly KB, MB, GB, or TB string."""
    B = float(B)
    KB = float(1024)
    MB = float(KB ** 2) # 1,048,576
    GB = float(KB ** 3) # 1,073,741,824
    TB = float(KB ** 4) # 1,099,511,627,776

    if B < KB:
        return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
    elif KB <= B < MB:
        return '{0:.2f} KB'.format(B / KB)
    elif MB <= B < GB:
        return '{0:.2f} MB'.format(B / MB)
    elif GB <= B < TB:
        return '{0:.2f} GB'.format(B / GB)
    elif TB <= B:
        return '{0:.2f} TB'.format(B / TB)


def humanizeTime(amount: float, units: str) -> str:
        """Divide `amount` in time periods.
            Useful for making time intervals more human readable.

        Args:
            amount (float): value time
            units (str): value unit

        Returns:
            str: time human readable
        """

        intervals = [
            1,
            1000,
            1000000,
            60000000,
            3600000000,
            86400000000,
            604800000000,
            2419200000000,
            29030400000000,
        ]
        names = [
            ("us", "us"),
            ("ms", "ms"),
            ("s", "s"),
            ("min", "min"),
            ("h", "h"),
            ("day", "days"),
            ("week", "weeks"),
            ("month", "months"),
            ("year", "years"),
        ]
        result = []

        unit = list(map(lambda a: a[1], names)).index(units)
        # Convert to seconds
        amount = amount * intervals[unit]

        for i in range(len(names) - 1, -1, -1):
            a = amount / intervals[i]
            if int(a) > 0:
                result.append((a, names[i][1 % int(a)]))
                amount -= a * intervals[i]

        return f"{result[0][0]:.2f} {result[0][1]}" if len(result) > 0 else ""