.model large ;Segmentos de 65 535 bytes
CURSOR MACRO ren, col
    mov ah, 2
    mov bh, 0
    mov dh, ren
    mov dl, col
    int 10h
ENDM
; Clear screen from (ren1, col1) to (ren2, col2)
CLS MACRO ren1, col1, ren2, col2, fondo
    mov ax, 0600h
    mov bh, fondo ; Style pointed by ptr
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

IMPCARB MACRO ren, col, car, color
    CURSOR ren,col
    mov ah, 9
    mov bh, 0
    mov cx, 1
    mov bl, color
    int 10h
ENDM

pila segment para stack 'stack'
    dw 64 dup(0)
pila ends

datos segment para 'data'
    tcabecera db "     [F2] Editar [F3] Buscar [F4] Reemplazar [F5] Limpiar pantalla [ESC] Fin", '$'
    ren db 00h
    col db 00h
    estilo1 db 01110000b ; fondo gris, letras negras
    estilo2 db 11110100b
datos ends

codigo segment para 'code'
    UI PROC NEAR
        CLS 0,0,0,79, 01110000b ;Cabecera fondo
        CLS 20,1,20,78, 10111111b ;barra inferior 1
        CLS 21,1,21,78, 01111111b ;barra inferior 2
        CLS 2,1,19,78, 00011000b
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
        call CABECERA 
        RET
    UI ENDP

    CABECERA PROC NEAR
        LEA si, tcabecera
        LEA di, ren ;direccion  a renglon
        mov word ptr [di], 0000h
        imprimeC:
            mov al, [si]
            cmp al, '$'
            JE salirC
            cmp al, '['
            JE  resaltarC
            IMPCAR [di], [di+1], al,
            inc byte ptr [di+1] ;Siguiente columna
            inc si
            sigueC:
            JMP imprimeC

        resaltarC:
            imprimeC2:
            mov al, [si]
            IMPCARB [di], [di+1], al, 11110100b
            inc byte ptr [di+1] ;Siguiente columna
            inc si
            cmp al, ']'
            JE sigueC
            JMP  imprimeC2

        salirC:
        RET
    CABECERA ENDP

    LEER PROC NEAR
        leerop:
            mov ah, 1
            int 21h

            cmp al, 39h
            JG leerop
            cmp al, 30h
            JL leerop
            sub al, 30h
            mov [di], al
        RET
    LEER ENDP

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
        call LEER
        RET
    Main ENDP
codigo ends
    end Main