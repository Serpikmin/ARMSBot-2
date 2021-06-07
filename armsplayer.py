class ArmsPlayer:     # Cringe-ass class, please ignore
    """
    A registered ARMS player.
    Has data for their friend code, region, main, and colour.
    """

    fc: str
    region: str
    main: str
    alt: int
    bg: int

    def __init__(self, fc: str, region: str, main="undecided", alt=1, bg=1) -> None:
        """Initialize an ARMS player."""
        self.fc = fc
        self.region = region
        self.main = main
        self.alt = alt
        self.bg = bg
