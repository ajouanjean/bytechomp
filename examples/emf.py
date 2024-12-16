from bytechomp import Reader, dataclass, Annotated
from bytechomp.datatypes import U8, U16, U32
from io import BytesIO


@dataclass
class PointL:
    x: U32
    y: U32


@dataclass
class RectL:
    TopLeft: PointL
    BottomRight: PointL


@dataclass
class SizeL:
    cx: U32
    cy: U32


@dataclass
class EMR_ArrayOfValues_TEST:
    Type: U32
    Size: U32
    NumberOfPolylines: U32
    aPolylinePointCount: Annotated[list[U32], 7]


@dataclass
class Header:
    Bounds: RectL
    Frame: RectL
    RecordSignature: U32
    Version: U32
    Bytes: U32
    Records: U32
    Handles: U16
    Reserved: U16
    nDescription: U32
    offDescription: U32
    nPalEntries: U32
    Device: SizeL
    Millimeters: SizeL
    cbPixelFormat: U32
    offPixelFormat: U32
    bOpenGL: U32
    MicrometersX: U32
    MicrometersY: U32


def test_array():
    ArrayOfValues_TEST_data = bytes.fromhex("""
        5A000000 
        74000000 
        07000000 
        02000000 03000000 04000000 05000000 02010000 08000000 0F000000 
        """)

    data = BytesIO(ArrayOfValues_TEST_data)

    klass = EMR_ArrayOfValues_TEST

    reader = Reader[klass]().allocate()

    # read from file until reader is satisfied
    with data as fp:
        while not reader:
            reader << fp.read()

    # build header message
    print(reader.build())


def test_rectL():
    BYTES = b"\x01\x00\x00\x00\x0f\x00\x00\x00\x01\x01\x00\x00\x0c\x00\x00\x00"

    data = BytesIO(BYTES)

    reader = Reader[RectL]().allocate()

    # read from file until reader is satisfied
    with data as fp:
        while not reader:
            reader << fp.read()

    # build header message
    print(reader.build())


def test_header():
    header_data = bytes.fromhex("""
    01000000 
    68000000 
    00000000 00000000 230C0000 42050000 
    FDFFFFFF FDFFFFFF 69330000 3C160000 
    20454D46 
    00000100 
    7C170000 
    5D000000 
    0500
    0000 
    00000000 
    00000000 
    00000000 
    EC130000 C8190000 
    D8000000 17010000 
    00000000 
    00000000 
    00000000 
    5C4B0300 
    68430400
    """)
    data = BytesIO(header_data)

    reader = Reader[Header]().allocate()

    # read from file until reader is satisfied
    with data as fp:
        while not reader:
            reader << fp.read()

    print(reader.build())


if __name__ == "__main__":
    test_header()
