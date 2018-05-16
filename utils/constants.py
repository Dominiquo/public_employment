RESULTS_BASE_LINK = "http://www.empleospublicos.cl/pub/convocatorias/convGanadores.aspx?i="
RESULTS_SUFFIX = '&t=OE'


EMPTY_PAGE = ''
POSTING_BASE_LINK = 'http://www.empleospublicos.cl/pub/convocatorias/'
INTERMEDIATE = '.aspx?i='
TYPE_LIST = ['convbasejefedpto',
			'avisotrabajoficha',
			'avisopizarronficha',
			'convbaseingplanta']


STORE_POSTINGS = '../stored_pages'


# PARSING HTML PAGES
ROW = 'tr'
CELL = 'td'
LIST_ITEM = 'li'
BOLD_TAG = 'b'
TABLE = 'table'
FASE = 'Fase'
UNORDERED_BULLET = 'ul'


DT_FORMAT = '%d/%m/%Y'
CALENDAR = 'calendar'


# JSON CONSTANTS
CALENDAR = 'CALENDAR'
MAIN_FIELDS = 'MAIN_FIELDS'
DAYS_OPEN = 'DAYS_OPEN'
DAYS_SELECT = 'DAYS_SELECT'
PROC_TIME = 'DAYS_PROC'

# COLUMNS
RESULTS = 'RESULTS'
ID_FIELD = 'PAGE_ID'
RESULTS = 'RESULTS' 
YEAR = 'YEAR'
MONTH = 'MONTH'
RESULT_CAT = 'RESULT_CAT'
WAGE_OG = 'Renta Bruta'
WAGE_V = 'WAGE'
MINISTRY = 'Ministerio'
MINISTRY_VAL = 'personnel_budget'

# RESULTS CATEGORIES
DESIERTO = 'EMPLEO DECLARADO DESIERTO'
SIN_RESULTADO = 'EMPLEO AÚN SIN RESULTADO'
SIN_EFECTO = 'EMPLEO DEJADO SIN EFECTO'

#plotting constants
SIZE = 'norm_size'
VACANCIES = 'NÂº de Vacantes'
SUM_COL = 'sum'
VAC_TYP = 'Tipo de Vacante'
TIME_OBJ = 'month_year'


#MINISTRY MAPPING
MINISTRY_MAP = {'Ministerio del Deporte': 'MINISTERIO DEL DEPORTE', 
				'Ministerio de Salud': 'MINISTERIO DEL SALUD',
				'Ministerio de EconomÃ\xada, Fomento y Turismo': 'MINISTERIO DE ECONOMÍA FOMENTO Y TURISMO',
				'Ministerio de Vivienda y Urbanismo': 'MINISTERIO DE VIVIENDA Y URBANISMO',
				'Ministerio de Defensa Nacional': 'MINISTERIO DE DEFENSA NACIONAL',
				'Ministerio de Hacienda': 'MINISTERIO DE HACIENDA',
				'Ministerio de Justicia y Derechos Humanos': 'MINISTERIO DE JUSTICIA Y DERECHOS HUMANOS',
				'Ministerio del Interior y Seguridad PÃºblica': 'MINISTERIO DEL INTERIOR Y SEGURIDAD PÚBLICA',
				'Ministerio de EducaciÃ³n': 'MINISTERIO DE EDUCACIÓN',
				'Ministerio de Desarrollo Social': 'MINISTERIO DE DESARROLLO SOCIAL', 
				'Ministerio de Agricultura': 'MINISTERIO DE AGRICULTURA',
				'Ministerio de Obras PÃºblicas': 'MINISTERIO DE OBRAS PÚBLICAS',
				'Ministerio de Transportes y Telecomunicaciones': 'MINISTERIO DE TRANSPORTES Y TELECOMUNICACIONES',
				'Ministerio de EnergÃ\xada': 'MINISTERIO DE ENERGÍA',
				'AutÃ³nomo': 'Autónomo',
				'Ministerio del Medio Ambiente': 'MINISTERIO DEL MEDIO AMBIENTE',
				'Ministerio de MinerÃ\xada': 'MINISTERIO DE MINERÍA',
				'Ministerio del Trabajo y PrevisiÃ³n Social': 'MINISTERIO DEL TRABAJO Y PREVISIÓN SOCIAL',
				'Ministerio de Bienes Nacionales': 'MINISTERIO DE BIENES NACIONALES', 
				'Ministerio de Relaciones Exteriores': 'MINISTERIO DE RELACIONES EXTERIORES',
				'Ministerio de la Mujer y la Equidad de GÃ©nero': 'MINISTERIO DE LA MUJER Y LA EQUIDAD DE GÉNERO',
				'Ministerio SecretarÃ\xada General de la Presidencia': 'MINISTERIO SECRETARÍA GENERAL DE LA PRESIDENCIA DE LA REPÚBLICA',
				'Ministerio SecretarÃ\xada General de Gobierno': 'MINISTERIO SECRETARÍA GENERAL DE GOBIERNO',
				'Ministerio de PlanificaciÃ³n': ''}


# 'NÂº de Vacantes' : 'Number_Vacancies'
# CÃ³digo del Trabajo -- VACAncy type
