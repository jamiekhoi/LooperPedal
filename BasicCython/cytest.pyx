import time
import numpy as np
cimport numpy as np
from copy import copy

dtype = 'int16'

def cytestMix(bytes audio1,bytes audio2):
    """
    0.015712976455688477 not looping, 1024 chunks

    """
    #cdef int size = 2000
    #cdef int p[size]
    decodeddata1 = copy(np.frombuffer(audio1, dtype=dtype))
    decodeddata2 = copy(np.frombuffer(audio2, dtype=dtype))
    #len(bytes(CHUNK))
    #len(decodeddata1)
    # This opperation is too slow making the noise garbage
    newdata = (decodeddata2 * 0.5 + decodeddata2 * 0.5).astype(int).tobytes()
    return newdata


