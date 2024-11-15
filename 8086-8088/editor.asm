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

IMPREP MACRO ren2, col2, cont, car
    CURSOR ren2, col2
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
    ren db 0
    col db 0
    estilo1 db 01110000b ; fondo gris, letras negras
    estilo2 db 00011000b
datos ends

codigo segment para 'code'
    UI PROC NEAR
        LEA si, estilo1
        CLS 0,0,0,79, si ;Cabecera fondo
        ; Primer margen superior
        IMPCAR 1, 0, 218 ;  Esquina superior izquierda           
        IMPREP 1, 1, 78, 196
        IMPCAR 1, 79, 191 ; Esquina superior derecha   
        mov cx, 21 ; Iteraciones
        LEA  si, ren
        mov [si], 2
        looplado2:
            IMPCAR [si], 0, 179
            IMPCAR [si], 79, 179
            inc byte ptr [si]
        loop looplado2
        IMPCAR 22, 0, 192 ;  Esquina inferior izquierda           
        IMPREP 22, 1, 78, 196
        IMPCAR 22, 79, 217 ; Esquina inferior derecha 
        RET
    UI ENDP

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
        call UI
        RET
    Main ENDP
codigo ends
    end Main