"""
    Serialize & Deserialize OY response
    _____________________________________
    serialize all of response to prevent all changes from oy side breaking the
    libs
"""
from marshmallow import Schema, fields, EXCLUDE


class InquiryAccountSchema(Schema):
    """ used to serialize oy inquiry account response """
    bank_code = fields.Str(data_key="recipient_bank")
    account_no = fields.Str(data_key="recipient_account")
    name = fields.Str(data_key="recipient_name")

    class Meta:
        unknown = EXCLUDE


class DisburseSchema(Schema):
    """ used to serialize oy disburse response """
    bank_code = fields.Str(data_key="recipient_bank")
    account_no = fields.Str(data_key="recipient_account")
    amount = fields.Decimal()
    trx_reference = fields.Str(data_key="trx_id") # trx id genertaed from oy

    class Meta:
        unknown = EXCLUDE


class DisburseStatusSchema(Schema):
    """ used to serialize oy disburse response """
    name = fields.Str(data_key="recipient_name")
    bank_code = fields.Str(data_key="recipient_bank")
    account_no = fields.Str(data_key="recipient_account")
    trx_id = fields.Str(data_key="partner_trx_id")  # the one we request to oy
    trx_reference = fields.Str(data_key="trx_id")  # the one we recevie from oy
    amount = fields.Decimal()
    timestamp = fields.DateTime(format='%d-%m-%Y %H:%M:%S')
    created_date = fields.DateTime(format='%d-%m-%Y %H:%M:%S')
    last_updated_date = fields.DateTime(format='%d-%m-%Y %H:%M:%S')

    class Meta:
        unknown = EXCLUDE


class GetBalanceSchema(Schema):
    """ used to serialize oy get balance response """
    balance = fields.Decimal()

    class Meta:
        unknown = EXCLUDE


class GenerateVaSchema(Schema):
    """ used to serialize oy generate va no response """
    va_no = fields.Str(data_key="vaNumber")
    amount = fields.Decimal()

    class Meta:
        unknown = EXCLUDE
