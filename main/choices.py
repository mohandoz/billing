from decimal import Decimal

ACTIVE = 1
INACTIVE = 2
DELETED = 3

STATUS_CHOICE = (
    (ACTIVE, "فعال"),
    (INACTIVE, "غير فعال"),
    # (DELETED, "Deleted"),
# ('', 'الكل'),
)




LOCATOIN_CHOICE = (
    ("Amman", "Amman"),
)

DISCOUNT_CHOICE = (
    (Decimal("0.0"), "No discount"),
    (Decimal("0.1"), "% 10"),
    (Decimal("0.2"), "% 20"),
    (Decimal("0.3"), "% 30"),
    (Decimal("0.4"), "% 40"),
    (Decimal("0.5"), "% 50"),
)

