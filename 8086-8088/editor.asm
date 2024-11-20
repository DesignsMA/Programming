.model large ;Segmentos de 65 535 bytes
CURSOR MACRO ren, col
    mov ah, 2
    mov bh, 0
    mov dh, ren
    mov dl, col
    int 10h
ENDM
; Borrar pantalla de (ren1,col1) a (ren2, col2), fondo
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

LEER MACRO ren, col, ptrv
    CURSOR ren, col
    mov ah, 10h
    int 16h
    cmp ah, 0EH
    JE backspace
    cmp ah, 01
    JE finMain
    cmp ah, 4bh
    JE dirIz
    cmp ah, 4dh
    JE dirDer
    ;Comparando con teclas especiales
    ;cmp [si], 3BH
    ;je f1
    ;cmp [si], 3CH
    ;je f2
    ;cmp [si], 3DH
    ;je f3
    ;cmp [si], 3EH
    ;je f4
    ;cmp [si], 3FH
    ;je f5
    mov byte ptr [ptrv], al
ENDM

LIMPIARMEM MACRO
    LEA DI, tcuerpo       ; Cargar la dirección del arreglo.
    MOV CX, 10           ; Número de bytes a limpiar.
    MOV AL, 0            ; Valor 0 a llenar.
    REP STOSB            ; Limpiar el arreglo llenando con 0.
ENDM

pila segment para stack 'stack'
    dw 64 dup(0)
pila ends

datos segment para 'data'
    ren db 0
    col db 0
    estilo1 db 01110000b ; fondo gris, letras negras
    estilo2 db 11110100b
    tcabecera db "     [F2] Editar [F3] Buscar [F4] Reemplazar [F5] Limpiar pantalla [ESC] Fin", '$'
    tcuerpo db 1404 dup(0), '$' ;Almacenando memoria de  el texto escrito
datos ends

codigo segment para 'code'
    UI PROC NEAR
        CLS 0,0,0,79, 01110000b ;Cabecera fondo
        CLS 20,1,20,78, 10111111b ;barra inferior 1
        CLS 21,1,21,78, 01111111b ;barra inferior 2
        CLS 2,1,19,78, 00011111b
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
        LEA si, tcuerpo ; Direccion al cuerpo de texto
        LEA di, ren ; Direccion a renglon  y columna
        mov byte ptr [di], 2 ;iniciar el columna 1, renglon 2
        mov byte ptr [di+1], 1
        editor:
            cmp byte ptr [si], '$' ;Si se llego al final del cuerpo
            JE reset
            
            LEER [di], [di+1], si ;Renglon, columna, actualiza el cuerpo
            IMPCARB [di], [di+1], [si], 00011111b 
            inc si
            inc byte ptr [di+1] 
            cmp byte ptr [di+1], 79  ;Si se llega al final de la columna
            JE sigRen
            editorf:
            jmp editor

        sigRen:
        inc byte ptr [di]
        mov byte ptr [di+1], 1
        jmp editorf
        
        reset:
        mov byte ptr [di], 2
        mov byte ptr [di+1], 1
        LEA si, tcuerpo ;Empezar en caracter cero
        jmp editorf

        backspace:
            cmp byte ptr [di+1], 1 ; Si es la primera columna
            JE renAnterior
            dec byte ptr [di+1] ;columna anterior
            mov byte ptr [si], 0
            dec si
            CLS [di], [di+1], [di], [di+1], 00011111b
            jmp editorf

        renAnterior:
            cmp byte ptr [di], 2
            JE editorf
            dec byte ptr [di]
            mov byte ptr [di+1], 79
            buscaCar:
                cmp byte ptr [di+1], 1
                JE terminaBusca
                dec si
                dec byte  ptr [di+1]
                cmp byte ptr [si], 0 ; mientras sea vacio
                JE buscaCar
            terminaBusca:
            mov byte ptr [si], 0
            CLS [di], [di+1], [di], [di+1], 00011111b
            jmp editorf

        enter:
        
        dirIz:
            dec si
            cmp byte ptr [di+1],1
            JE dirIz1
            dec byte ptr [di+1]
            jmp editor
            dirIz1:
                cmp byte  ptr [di], 2
                JE dirIz2
                mov byte ptr [di+1], 78
                dec byte ptr [di] ;renglon anterior
                dirIz2:
                jmp editor

        dirDer:
            inc si
            cmp byte ptr [di+1],78
            JE dirDer1
            inc byte ptr [di+1]
            jmp editor
            dirDer1:
                cmp byte  ptr [di], 19
                JE dirDer2
                mov byte ptr [di+1], 1
                inc byte ptr [di] ;siguiente renglon
                dirDer2:
                jmp editor
        
        
        finMain:
        RET
    Main ENDP
codigo ends
    end Main