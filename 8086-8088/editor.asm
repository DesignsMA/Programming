.model large
CURSOR MACRO ren, col
    mov ah, 2
    mov bh, 0
    mov dh, ren
    mov dl, col
    int 10h
ENDM

; Clear screen from (ren1, col1) to (ren2, col2)
CLS MACRO ren1, col1, ren2, col2, ptrv
    mov ax, 0600h
    mov bh, [ptrv] ; Style pointed by ptr
    mov ch, ren1
    mov cl, col1
    mov dh, ren2
    mov dl, col2
    int 10h
ENDM

IMPCAD MACRO ptrv
    mov ah, 09h
    lea dx, ptrv
    int 21h
ENDM

IMPREP MACRO ren, col, cont, car
    CURSOR ren, col
    mov dl, car
    repeat cont
    int 21h
    endm
ENDM

IMPCAR MACRO ren, col, car
    CURSOR ren, col
    mov dl, car
    int 21h
ENDM

pila segment para stack 'stack'
    dw 64 dup(0)
pila ends

datos segment para 'data'
    estilo1 db 01001000b
    estilo2 db 00011000b
datos ends

codigo segment para 'code'

    Main PROC FAR
        assume cs:codigo, ds:datos, ss:pila
        ; Protocolo
        push ds
        sub ax,ax
        push ax
        mov ax, datos
        mov ds, ax
        mov es, ax
        ; - 
        LEA SI, estilo1
        CLS 0, 0, 2, 10,si
        LEA SI, estilo2
        CLS 3, 0, 5, 10,si
        IMPREP 0,0, 79, 41h
        IMPREP 4,0, 79, 42h
        HLT
    Main ENDP
codigo ends
    end Main