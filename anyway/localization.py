#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import os
from . import field_names
import six
from functools import partial


_tables = {
    "SUG_DEREH": {
        1: "עירוני בצומת",
        2: "עירוני לא בצומת",
        3: "לא עירוני בצומת",
        4: "לא עירוני לא בצומת",
    },
    "YEHIDA": {
        11: "מרחב חוף (חיפה)",
        12: "מרחב גליל",
        14: "מרחב עמקים",
        20: "מרחב ת\"א",
        33: "מרחב אילת",
        34: "מרחב הנגב",
        36: "מרחב שמשון (עד 1999)",
        37: "מרחב שמשון (החל ב-2004)",
        38: "מרחב לכיש",
        41: "מרחב שומרון",
        43: "מרחב יהודה",
        51: "מרחב השרון",
        52: "מרחב השפלה",
        61: "מחוז ירושלים",
    },
    "SUG_YOM": {
        1: "חג",
        2: "ערב חג",
        3: "חול המועד",
        4: "יום אחר",
    },
    "HUMRAT_TEUNA": {
        1: "קטלנית",
        2: "קשה",
        3: "קלה",
    },
    "SUG_TEUNA": {
        1: "פגיעה בהולך רגל",
        2: "התנגשות חזית אל צד",
        3: "התנגשות חזית באחור",
        4: "התנגשות צד בצד",
        5: "התנגשות חזית אל חזית",
        6: "התנגשות עם רכב שנעצר ללא חניה",
        7: "התנגשות עם רכב חונה",
        8: "התנגשות עם עצם דומם",
        9: "ירידה מהכביש או עלייה למדרכה",
        10: "התהפכות",
        11: "החלקה",
        12: "פגיעה בנוסע בתוך כלי רכב",
        13: "נפילה ברכב נע",
        14: "שריפה",
        15: "אחר",
        17: "התנגשות אחור אל חזית",
        18: "התנגשות אחור אל צד",
        19: "התנגשות עם בעל חיים",
        20: "פגיעה ממטען של רכב",
    },
    "ZURAT_DEREH": {
        1: "כניסה למחלף",
        2: "ביציאה ממחלף",
        3: "מ.חניה/ת. דלק",
        4: "שיפוע תלול",
        5: "עקום חד",
        6: "על גשר מנהרה",
        7: "מפגש מסילת ברזל",
        8: "כביש ישר/צומת",
        9: "אחר",
    },
    "HAD_MASLUL": {
        1: "חד סיטרי",
        2: "דו סיטרי+קו הפרדה רצוף",
        3: "דו סיטרי אין קו הפרדה רצוף",
        4: "אחר",
    },
    "RAV_MASLUL": {
        1: "מיפרדה מסומנת בצבע",
        2: "מיפרדה עם גדר בטיחות",
        3: "מיפרדה בנויה ללא גדר בטיחות",
        4: "מיפרדה לא בנויה",
        5: "אחר",
    },
    "MEHIRUT_MUTERET": {
        1: "עד 50 קמ\"ש",
        2: "60 קמ\"ש",
        3: "70 קמ\"ש",
        4: "80 קמ\"ש",
        5: "90 קמ\"ש",
        6: "100 קמ\"ש",
    },
    "TKINUT": {
        1: "אין ליקוי",
        2: "שוליים גרועים",
        3: "כביש משובש",
        4: "שוליים גרועים וכביש משובש",
    },
    "ROHAV": {
        1: "עד 5 מטר",
        2: "5 עד 7",
        3: "7 עד 10.5",
        4: "10.5 עד 14",
        5: "יותר מ-14",
    },
    "SIMUN_TIMRUR": {
        1: "סימון לקוי/חסר",
        2: "תימרור לקוי/חסר",
        3: "אין ליקוי",
        4: "לא נדרש תמרור",
    },
    "TEURA": {
        1: "אור יום רגיל",
        2: "ראות מוגבלת עקב מזג אויר (עשן,ערפל)",
        3: "לילה פעלה תאורה",
        4: "קיימת תאורה בלתי תקינה/לא פועלת",
        5: "לילה לא קיימת תאורה",
    },
    "BAKARA": {
        1: "אין בקרה",
        2: "רמזור תקין",
        3: "רמזור מהבהב צהוב",
        4: "רמזור לא תקין",
        5: "תמרור עצור",
        6: "תמרור זכות קדימה",
        7: "אחר",
    },
    "MEZEG_AVIR": {
        1: "בהיר",
        2: "גשום",
        3: "שרבי",
        4: "ערפילי",
        5: "אחר",
    },
    "PNE_KVISH": {
        1: "יבש",
        2: "רטוב ממים",
        3: "מרוח בחומר דלק",
        4: "מכוסה בבוץ",
        5: "חול או חצץ על הכביש",
        6: "אחר",
    },
    "SUG_EZEM": {
        1: "עץ",
        2: "עמוד חשמל/תאורה/טלפון",
        3: "תמרור ושלט",
        4: "גשר סימניו ומגיניו",
        5: "מבנה",
        6: "גדר בטיחות לרכב",
        7: "חבית",
        8: "אחר",
    },
    "MERHAK_EZEM": {
        1: "עד מטר",
        2: "1-3 מטר",
        3: "על הכביש",
        4: "על שטח הפרדה",
    },
    "LO_HAZA": {
        1: "הלך בכיוון התנועה",
        2: "הלך נגד",
        3: "שיחק על הכביש",
        4: "עמד על הכביש",
        5: "היה על אי הפרדה",
        6: "היה על שוליים/מדרכה",
        7: "אחר",
    },
    "OFEN_HAZIYA": {
        1: "התפרץ אל הכביש",
        2: "חצה שהוא מוסתר",
        3: "חצה רגיל",
        4: "אחר",
    },
    "MEKOM_HAZIYA": {
        1: "לא במעבר חציה ליד צומת",
        2: "לא במעבר חציה לא ליד צומת",
        3: "במעבר חציה בלי רמזור",
        4: "במעבר חציה עם רמזור",
    },
    "KIVUN_HAZIYA": {
        1: "מימין לשמאל",
        2: "משמאל לימין",
    },
    "STATUS_IGUN": {
        1: "עיגון מדויק",
        2: "מרכז ישוב",
        3: "מרכז דרך",
        4: "מרכז קילומטר",
        9: "לא עוגן",
    }
}

_fields = {
    "pk_teuna_fikt": "מזהה",
    "SUG_DEREH": "סוג דרך",
    "SHEM_ZOMET": "שם צומת",
    "SEMEL_YISHUV": "ישוב",  # from dictionary
    "REHOV1": "רחוב 1",  # from dicstreets (with SEMEL_YISHUV)
    "REHOV2": "רחוב 2",  # from dicstreets (with SEMEL_YISHUV)
    "BAYIT": "מספר בית",
    "ZOMET_IRONI": "צומת עירוני",  # from intersect urban dictionary
    "KVISH1": "כביש 1",  # from intersect urban dictionary
    "KVISH2": "כביש 2",  #from intersect urban dictionary
    "ZOMET_LO_IRONI": "צומת לא עירוני",  #from non urban dictionary
    "YEHIDA": "יחידה",
    "SUG_YOM": "סוג יום",
    "RAMZOR": "רמזור",
    "HUMRAT_TEUNA": "חומרת תאונה",
    "SUG_TEUNA": "סוג תאונה",
    "ZURAT_DEREH": "צורת דרך",
    "HAD_MASLUL": "חד מסלול",
    "RAV_MASLUL": "רב מסלול",
    "MEHIRUT_MUTERET": "מהירות מותרת",
    "TKINUT": "תקינות",
    "ROHAV": "רוחב",
    "SIMUN_TIMRUR": "סימון תמרור",
    "TEURA": "תאורה",
    "BAKARA": "בקרה",
    "MEZEG_AVIR": "מזג אוויר",
    "MEZEG_AVIR_UNITED": "מזג אוויר",
    "PNE_KVISH": "פני כביש",
    "SUG_EZEM": "סוג עצם",
    "MERHAK_EZEM": "מרחק עצם",
    "LO_HAZA": "לא חצה",
    "OFEN_HAZIYA": "אופן חציה",
    "MEKOM_HAZIYA": "מקום חציה",
    "KIVUN_HAZIYA": "כיוון חציה",
    "STATUS_IGUN": "עיגון",
    "MAHOZ": "מחוז",
    "NAFA": "נפה",
    "EZOR_TIVI": "אזור טבעי",
    "MAAMAD_MINIZIPALI": "מעמד מוניציפלי",
    "ZURAT_ISHUV": "צורת יישוב",
    "VEHICLE_TYPE": "סוג רכב",
    "VIOLATION_TYPE": "סוג עבירה"
}

if six.PY3:
    _open_hebrew_textfile = partial(open, encoding='cp1255')
else:
    _open_hebrew_textfile = open

if six.PY3:
    _decode_hebrew = lambda s: s
else:
    _decode_hebrew = lambda s: s.decode("cp1255")


with _open_hebrew_textfile(os.path.join("static/data/cities.csv"), "r") as f:
    _cities = list(csv.DictReader(f))

_cities_names = {int(x[field_names.sign]): _decode_hebrew(x[field_names.name]) for x in _cities}


def get_field(field, value=None):
    if value:
        table = _tables.get(field, None)
        return table.get(value, None) if table else None

    return _fields.get(field, None)


def get_supported_tables():
    return _tables.keys()


def get_city_name(symbol_id):
    return _cities_names.get(symbol_id, None)
