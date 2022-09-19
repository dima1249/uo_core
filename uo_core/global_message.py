from django.utils.translation import gettext_lazy as _


class GlobalMessage(object):
    SUCCESS = _("Амжилттай")
    SAVE_ERROR = _("Хадгалахад алдаа гарлаа")
    ERROR = _("Aлдаа гарлаа")
    NO_DATA = _("Харгалзах үр дүн байхгүй байна")
    VALIDATION_ERROR = _("Хүсэлтийн өгөгдөл алдаатай байна")
    TOKEN_VALIDATOR_ERROR = _("Token алдаатай байна")

    MAINTENANCE_ERROR = _("СИСТЕМ ДЭЭР ЗАСВАР ХИЙГДЭЖ БАЙНА")
    GLOBAL_WEIGHT = _("кг")

    NOT_FOUND_ERROR = _("Олдсонгүй")

    # Gok
    INVOICE_CREATED = _("Нэхэмжлэл үүссэн.")
    INVOICE_PAID = _("Төлбөр төлөгдсөн.")
    INVOICE_ALREADY_PAID = _("Төлбөр төлөгдсөн.")
    INVOICE_NOT_FOUND = _("Нэхэмжлэл олдсонгүй.")
    INVOICE_NOT_PAID = _("Төлбөр төлөгдөөгүй байна.")
    INVOICE_NOT_CREATED = _("Нэхэмжлэл үүсгэж чадсангүй.")
    INVOICE_ALREADY_CREATED = _("Үүсгэгдсэн нэхэмжлэл байна.")
    # payment response
    PAYMENT_SUCCESS = _("Төлбөр амжилттай.")
    PAYMENT_SUCCESS_DESCRIPTION = _("Төлбөр амжилттай хийгдлээ.")
    PAYMENT_UNSUCCESS = _("Төлбөр амжилтгүй.")
    PAYMENT_UNSUCCESS_DESCRIPTION = _("Төлбөр амжилтгүй боллоо!")

    PAYMENT_ORDER_NOT_FOUND = _("Захиалгын мэдээлэл олдсонгүй")
    PAYMENT_NOT_FOUND = _("Төлбөрийн төрөл олдсонгүй.")

    # Order mail message
    ORDER_CREATED_MAIL_TITLE = _(" захиалга үүслээ")
    ORDER_CREATED_MAIL_BODY = _(
        "Сайн байна уу? Таны захиалга амжилттай үүслээ. Та төлбөрөө төлж баталгаажуулна уу! 30 минутын дотор баталгаажуулаагүй тохиолдолд захиалга автоматаар цуцлагдана.")
    ORDER_PAYMENT_PAID = _(" дугаартай төлбөр төлөгдлөө")
    # Booking
    CHECK_COMPANY_REGISTER = _("Компанийн регистр шалгана уу")
    CHECK_BOOKING_PAX = _("Зорчигчдын мэдээллийг шалгана уу")
    CHECK_PERSONAL_REGISTER = _("Регистрийн дугаараа шалгана уу")
    INFANT_NOT_INCLUDED = _("Нярай оруулах боломжгүй")

    TOO_MANY_INFANTS = _("Нярай зорчигчийн тоо насанд хүрсэн зорчигчийн тооноос олон байж болохгүй.")
    TOO_MANY_PASSENGERS = _("Есөөс олон тооны зорчигчоор хайлт хийх боломжгүй.")
    FUTURE_DATE_SEARCH = _("Зөвхөн өнөөдрөөс 361 өдрийн дотор хайлт хийх боломжтой.")

    NOT_ADULT_AERO = _("Нярай зорчигчид харгалзах зорчигч нь 16 ба түүнээс дээш настай байх ёстой.")
    NOT_ADULT_SABRE = _("Нярай зорчигчид харгалзах зорчигч нь 18 ба түүнээс дээш настай байх ёстой.")
