from _external import *


if not windows:
	pthread = LibWithHeaderChecker('pthread', 'pthread.h', 'c', call='pthread_attr_t attr;pthread_attr_init(&attr);')
else:
	pthread = ObjectChecker('pthread')

