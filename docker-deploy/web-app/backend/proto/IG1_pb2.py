# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: IG1.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='IG1.proto',
  package='IG1',
  syntax='proto2',
  serialized_pb=_b('\n\tIG1.proto\x12\x03IG1\"f\n\x04\x41Msg\x12#\n\nasendtruck\x18\x01 \x03(\x0b\x32\x0f.IG1.ASendTruck\x12+\n\x0e\x61\x66inishloading\x18\x02 \x03(\x0b\x32\x13.IG1.AFinishLoading\x12\x0c\n\x04\x61\x63ks\x18\x03 \x03(\x03\"\xba\x01\n\x04UMsg\x12\'\n\x0cuorderplaced\x18\x01 \x03(\x0b\x32\x11.IG1.UOrderPlaced\x12)\n\rutruckarrived\x18\x02 \x03(\x0b\x32\x12.IG1.UTruckArrived\x12)\n\rupkgdelivered\x18\x03 \x03(\x0b\x32\x12.IG1.UPkgDelivered\x12%\n\tinitworld\x18\x04 \x01(\x0b\x32\x12.IG1.UInitialWorld\x12\x0c\n\x04\x61\x63ks\x18\x05 \x03(\x03\"-\n\rUInitialWorld\x12\x0f\n\x07worldid\x18\x01 \x02(\x03\x12\x0b\n\x03seq\x18\x02 \x02(\x03\"\x91\x01\n\nASendTruck\x12\"\n\x06whinfo\x18\x01 \x02(\x0b\x32\x12.IG1.WarehouseInfo\x12\t\n\x01x\x18\x02 \x02(\x05\x12\t\n\x01y\x18\x03 \x02(\x05\x12\r\n\x05pkgid\x18\x04 \x02(\x03\x12\x1e\n\x08products\x18\x05 \x03(\x0b\x32\x0c.IG1.Product\x12\r\n\x05upsid\x18\x06 \x01(\t\x12\x0b\n\x03seq\x18\x07 \x02(\x03\"3\n\rWarehouseInfo\x12\x0c\n\x04whid\x18\x01 \x02(\x05\x12\t\n\x01x\x18\x02 \x02(\x05\x12\t\n\x01y\x18\x03 \x02(\x05\"9\n\x07Product\x12\n\n\x02id\x18\x01 \x02(\x03\x12\x13\n\x0b\x64\x65scription\x18\x02 \x02(\t\x12\r\n\x05\x63ount\x18\x03 \x02(\x05\";\n\x0cUOrderPlaced\x12\r\n\x05pkgid\x18\x01 \x02(\x03\x12\x0f\n\x07truckid\x18\x02 \x02(\x05\x12\x0b\n\x03seq\x18\x03 \x02(\x03\"-\n\rUTruckArrived\x12\x0f\n\x07truckid\x18\x01 \x02(\x05\x12\x0b\n\x03seq\x18\x02 \x02(\x03\"=\n\x0e\x41\x46inishLoading\x12\r\n\x05pkgid\x18\x01 \x02(\x03\x12\x0f\n\x07truckid\x18\x02 \x02(\x05\x12\x0b\n\x03seq\x18\x03 \x02(\x03\"+\n\rUPkgDelivered\x12\r\n\x05pkgid\x18\x01 \x02(\x03\x12\x0b\n\x03seq\x18\x02 \x02(\x03')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_AMSG = _descriptor.Descriptor(
  name='AMsg',
  full_name='IG1.AMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='asendtruck', full_name='IG1.AMsg.asendtruck', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='afinishloading', full_name='IG1.AMsg.afinishloading', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='acks', full_name='IG1.AMsg.acks', index=2,
      number=3, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=18,
  serialized_end=120,
)


_UMSG = _descriptor.Descriptor(
  name='UMsg',
  full_name='IG1.UMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='uorderplaced', full_name='IG1.UMsg.uorderplaced', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='utruckarrived', full_name='IG1.UMsg.utruckarrived', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='upkgdelivered', full_name='IG1.UMsg.upkgdelivered', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='initworld', full_name='IG1.UMsg.initworld', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='acks', full_name='IG1.UMsg.acks', index=4,
      number=5, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=123,
  serialized_end=309,
)


_UINITIALWORLD = _descriptor.Descriptor(
  name='UInitialWorld',
  full_name='IG1.UInitialWorld',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='worldid', full_name='IG1.UInitialWorld.worldid', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='seq', full_name='IG1.UInitialWorld.seq', index=1,
      number=2, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=311,
  serialized_end=356,
)


_ASENDTRUCK = _descriptor.Descriptor(
  name='ASendTruck',
  full_name='IG1.ASendTruck',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='whinfo', full_name='IG1.ASendTruck.whinfo', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='x', full_name='IG1.ASendTruck.x', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='y', full_name='IG1.ASendTruck.y', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='pkgid', full_name='IG1.ASendTruck.pkgid', index=3,
      number=4, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='products', full_name='IG1.ASendTruck.products', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='upsid', full_name='IG1.ASendTruck.upsid', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='seq', full_name='IG1.ASendTruck.seq', index=6,
      number=7, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=359,
  serialized_end=504,
)


_WAREHOUSEINFO = _descriptor.Descriptor(
  name='WarehouseInfo',
  full_name='IG1.WarehouseInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='whid', full_name='IG1.WarehouseInfo.whid', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='x', full_name='IG1.WarehouseInfo.x', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='y', full_name='IG1.WarehouseInfo.y', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=506,
  serialized_end=557,
)


_PRODUCT = _descriptor.Descriptor(
  name='Product',
  full_name='IG1.Product',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='IG1.Product.id', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='description', full_name='IG1.Product.description', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='count', full_name='IG1.Product.count', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=559,
  serialized_end=616,
)


_UORDERPLACED = _descriptor.Descriptor(
  name='UOrderPlaced',
  full_name='IG1.UOrderPlaced',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='pkgid', full_name='IG1.UOrderPlaced.pkgid', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='truckid', full_name='IG1.UOrderPlaced.truckid', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='seq', full_name='IG1.UOrderPlaced.seq', index=2,
      number=3, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=618,
  serialized_end=677,
)


_UTRUCKARRIVED = _descriptor.Descriptor(
  name='UTruckArrived',
  full_name='IG1.UTruckArrived',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='truckid', full_name='IG1.UTruckArrived.truckid', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='seq', full_name='IG1.UTruckArrived.seq', index=1,
      number=2, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=679,
  serialized_end=724,
)


_AFINISHLOADING = _descriptor.Descriptor(
  name='AFinishLoading',
  full_name='IG1.AFinishLoading',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='pkgid', full_name='IG1.AFinishLoading.pkgid', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='truckid', full_name='IG1.AFinishLoading.truckid', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='seq', full_name='IG1.AFinishLoading.seq', index=2,
      number=3, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=726,
  serialized_end=787,
)


_UPKGDELIVERED = _descriptor.Descriptor(
  name='UPkgDelivered',
  full_name='IG1.UPkgDelivered',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='pkgid', full_name='IG1.UPkgDelivered.pkgid', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='seq', full_name='IG1.UPkgDelivered.seq', index=1,
      number=2, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=789,
  serialized_end=832,
)

_AMSG.fields_by_name['asendtruck'].message_type = _ASENDTRUCK
_AMSG.fields_by_name['afinishloading'].message_type = _AFINISHLOADING
_UMSG.fields_by_name['uorderplaced'].message_type = _UORDERPLACED
_UMSG.fields_by_name['utruckarrived'].message_type = _UTRUCKARRIVED
_UMSG.fields_by_name['upkgdelivered'].message_type = _UPKGDELIVERED
_UMSG.fields_by_name['initworld'].message_type = _UINITIALWORLD
_ASENDTRUCK.fields_by_name['whinfo'].message_type = _WAREHOUSEINFO
_ASENDTRUCK.fields_by_name['products'].message_type = _PRODUCT
DESCRIPTOR.message_types_by_name['AMsg'] = _AMSG
DESCRIPTOR.message_types_by_name['UMsg'] = _UMSG
DESCRIPTOR.message_types_by_name['UInitialWorld'] = _UINITIALWORLD
DESCRIPTOR.message_types_by_name['ASendTruck'] = _ASENDTRUCK
DESCRIPTOR.message_types_by_name['WarehouseInfo'] = _WAREHOUSEINFO
DESCRIPTOR.message_types_by_name['Product'] = _PRODUCT
DESCRIPTOR.message_types_by_name['UOrderPlaced'] = _UORDERPLACED
DESCRIPTOR.message_types_by_name['UTruckArrived'] = _UTRUCKARRIVED
DESCRIPTOR.message_types_by_name['AFinishLoading'] = _AFINISHLOADING
DESCRIPTOR.message_types_by_name['UPkgDelivered'] = _UPKGDELIVERED

AMsg = _reflection.GeneratedProtocolMessageType('AMsg', (_message.Message,), dict(
  DESCRIPTOR = _AMSG,
  __module__ = 'IG1_pb2'
  # @@protoc_insertion_point(class_scope:IG1.AMsg)
  ))
_sym_db.RegisterMessage(AMsg)

UMsg = _reflection.GeneratedProtocolMessageType('UMsg', (_message.Message,), dict(
  DESCRIPTOR = _UMSG,
  __module__ = 'IG1_pb2'
  # @@protoc_insertion_point(class_scope:IG1.UMsg)
  ))
_sym_db.RegisterMessage(UMsg)

UInitialWorld = _reflection.GeneratedProtocolMessageType('UInitialWorld', (_message.Message,), dict(
  DESCRIPTOR = _UINITIALWORLD,
  __module__ = 'IG1_pb2'
  # @@protoc_insertion_point(class_scope:IG1.UInitialWorld)
  ))
_sym_db.RegisterMessage(UInitialWorld)

ASendTruck = _reflection.GeneratedProtocolMessageType('ASendTruck', (_message.Message,), dict(
  DESCRIPTOR = _ASENDTRUCK,
  __module__ = 'IG1_pb2'
  # @@protoc_insertion_point(class_scope:IG1.ASendTruck)
  ))
_sym_db.RegisterMessage(ASendTruck)

WarehouseInfo = _reflection.GeneratedProtocolMessageType('WarehouseInfo', (_message.Message,), dict(
  DESCRIPTOR = _WAREHOUSEINFO,
  __module__ = 'IG1_pb2'
  # @@protoc_insertion_point(class_scope:IG1.WarehouseInfo)
  ))
_sym_db.RegisterMessage(WarehouseInfo)

Product = _reflection.GeneratedProtocolMessageType('Product', (_message.Message,), dict(
  DESCRIPTOR = _PRODUCT,
  __module__ = 'IG1_pb2'
  # @@protoc_insertion_point(class_scope:IG1.Product)
  ))
_sym_db.RegisterMessage(Product)

UOrderPlaced = _reflection.GeneratedProtocolMessageType('UOrderPlaced', (_message.Message,), dict(
  DESCRIPTOR = _UORDERPLACED,
  __module__ = 'IG1_pb2'
  # @@protoc_insertion_point(class_scope:IG1.UOrderPlaced)
  ))
_sym_db.RegisterMessage(UOrderPlaced)

UTruckArrived = _reflection.GeneratedProtocolMessageType('UTruckArrived', (_message.Message,), dict(
  DESCRIPTOR = _UTRUCKARRIVED,
  __module__ = 'IG1_pb2'
  # @@protoc_insertion_point(class_scope:IG1.UTruckArrived)
  ))
_sym_db.RegisterMessage(UTruckArrived)

AFinishLoading = _reflection.GeneratedProtocolMessageType('AFinishLoading', (_message.Message,), dict(
  DESCRIPTOR = _AFINISHLOADING,
  __module__ = 'IG1_pb2'
  # @@protoc_insertion_point(class_scope:IG1.AFinishLoading)
  ))
_sym_db.RegisterMessage(AFinishLoading)

UPkgDelivered = _reflection.GeneratedProtocolMessageType('UPkgDelivered', (_message.Message,), dict(
  DESCRIPTOR = _UPKGDELIVERED,
  __module__ = 'IG1_pb2'
  # @@protoc_insertion_point(class_scope:IG1.UPkgDelivered)
  ))
_sym_db.RegisterMessage(UPkgDelivered)


# @@protoc_insertion_point(module_scope)
