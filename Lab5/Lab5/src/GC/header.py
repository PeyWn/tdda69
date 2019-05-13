def header_get_garbage_flag(heap, pointer):
    return ((heap[pointer+3] & 128) >> 7) == 1

def header_set_garbage_flag(heap, pointer, value):
    gf = header_get_garbage_flag(heap, pointer)
    if (value and gf) or (not value and not gf):
        return heap
    heap[pointer+3] = (heap[pointer+3] ^ 128)
    return heap

def header_get_used_flag(heap, pointer):
    return ((heap[pointer+3] & 64) >> 6) == 1

def header_set_used_flag(heap, pointer, value):
    uf = header_get_used_flag(heap, pointer)
    if (value and uf) or (not value and not uf):
        return heap
    heap[pointer+3] = (heap[pointer+3] ^ 64)
    return heap

def header_is_pointers_array(heap, pointer):
    return ((heap[pointer+3] & 32) >> 5) == 1


def header_mark_as_pointers_array(heap, pointer):
    heap[pointer+3] = (heap[pointer+3] | 32)
    return heap

def header_mark_as_bytes_array(heap, pointer):
    heap[pointer+3] = (heap[pointer+3] & 223)
    return heap

def header_get_size(heap, pointer):
    header = heap[pointer : pointer+4]
    header[3] = header[3] & 31
    MemSize = int.from_bytes(header, byteorder='little')
    return MemSize

def header_set_size(heap, pointer, size):
    header = heap[pointer : pointer+4]
    hsize = hex(size)
    for i in range(len(bina)):
        print(hsize[-i])
        print(header[-i])
