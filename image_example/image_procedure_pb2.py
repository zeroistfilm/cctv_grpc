# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: image_procedure.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='image_procedure.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x15image_procedure.proto\"<\n\x0cImageRequest\x12\x0c\n\x04\x66\x61rm\x18\x01 \x01(\t\x12\x0e\n\x06sector\x18\x02 \x01(\t\x12\x0e\n\x06\x63\x61mIdx\x18\x03 \x01(\t\"$\n\rImageResponse\x12\x13\n\x0bimageString\x18\x04 \x01(\x0c\x32:\n\x0bImageServer\x12+\n\x08getImage\x12\r.ImageRequest\x1a\x0e.ImageResponse\"\x00\x62\x06proto3'
)




_IMAGEREQUEST = _descriptor.Descriptor(
  name='ImageRequest',
  full_name='ImageRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='farm', full_name='ImageRequest.farm', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='sector', full_name='ImageRequest.sector', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='camIdx', full_name='ImageRequest.camIdx', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=25,
  serialized_end=85,
)


_IMAGERESPONSE = _descriptor.Descriptor(
  name='ImageResponse',
  full_name='ImageResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='imageString', full_name='ImageResponse.imageString', index=0,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=87,
  serialized_end=123,
)

DESCRIPTOR.message_types_by_name['ImageRequest'] = _IMAGEREQUEST
DESCRIPTOR.message_types_by_name['ImageResponse'] = _IMAGERESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ImageRequest = _reflection.GeneratedProtocolMessageType('ImageRequest', (_message.Message,), {
  'DESCRIPTOR' : _IMAGEREQUEST,
  '__module__' : 'image_procedure_pb2'
  # @@protoc_insertion_point(class_scope:ImageRequest)
  })
_sym_db.RegisterMessage(ImageRequest)

ImageResponse = _reflection.GeneratedProtocolMessageType('ImageResponse', (_message.Message,), {
  'DESCRIPTOR' : _IMAGERESPONSE,
  '__module__' : 'image_procedure_pb2'
  # @@protoc_insertion_point(class_scope:ImageResponse)
  })
_sym_db.RegisterMessage(ImageResponse)



_IMAGESERVER = _descriptor.ServiceDescriptor(
  name='ImageServer',
  full_name='ImageServer',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=125,
  serialized_end=183,
  methods=[
  _descriptor.MethodDescriptor(
    name='getImage',
    full_name='ImageServer.getImage',
    index=0,
    containing_service=None,
    input_type=_IMAGEREQUEST,
    output_type=_IMAGERESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_IMAGESERVER)

DESCRIPTOR.services_by_name['ImageServer'] = _IMAGESERVER

# @@protoc_insertion_point(module_scope)
