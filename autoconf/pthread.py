from _external import *

pthread = LibWithHeaderChecker('pthread', 'pthread.h', 'c', call='pthread_attr_t attr;pthread_attr_init(&attr);')
