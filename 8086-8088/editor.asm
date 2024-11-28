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

CLS2 MACRO ren1, col1, ren2, col2, fondo, bxcopy
    mov ax, 0600h
    mov bh, fondo ; Style pointed by ptr
    mov ch, ren1
    mov cl, col1
    mov dh, ren2
    mov dl, col2
    int 10h
    mov bx, [bxcopy]
ENDM

IMPCAD MACRO ptrv
    mov ah, 09h
    lea dx, ptrv
    int 21h
ENDM

IMPREP MACRO ren, col, cont, car
    local @et1
    CURSOR ren, col
    mov dl, car
    mov cx, cont
    @et1:
        int 21h
    loop @et1
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

CADHEX MACRO ptrcad, ptrnum
    mov dx, [ptrcad] ;mover  número : 12 -> 21 =  DX
    sub dx, 3030h
    mov al, dl ; mover 1
    mov ah, 10
    mul ah ; multiplica al*10
    add dh, al ;resultado en al, 10+2
    mov byte ptr [ptrnum], dh ;Mover número al apuntador
ENDM

LIMPIABARRAS MACRO
    CLS 20,1,20,78, 10111111b ;barra inferior 1
    CLS 21,1,21,78, 01111111b ;barra inferior 2
ENDM

LEERC MACRO  ptrv
        mov ah, 1h             ; Leer un carácter
        int 21h    
        mov byte ptr [ptrv], al ; Almacenar el carácter leído
ENDM

IMPRIMEBUFFER MACRO 
    local @loop1
    local @loop1ren
    local @loopcont
    lea si, tcuerpo
    lea di, ren
    mov byte ptr [di], 2
    mov byte ptr [di+1], 1
    mov cx, 1404
    
    @loop1:
        IMPCAR [di], [di+1], [si]
        inc byte ptr [di+1]
        inc si
        cmp byte ptr [di+1], 79
        je @loop1ren
        cmp byte ptr [di+1], 79
        jnz @loopcont
        @loop1ren:
        inc byte ptr [di]
        mov byte ptr [di+1], 1
        @loopcont:
    loop @loop1    
ENDM

LEERC2 MACRO ptrv, salto
        mov ah, 1h             ; Leer un carácter
        int 21h        
        ; Verificar si el carácter es Backspace (0x08)
        cmp al, 08h
        je salto             ; Si es Backspace, volver a leer

        ; Verificar si el carácter es Enter (0x0D)
        cmp al, 0Dh
        je salto            ; Si es Enter, volver a leer
        mov byte ptr [ptrv], al ; Almacenar el carácter leído
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
    cmp ah, 50h
    JE dirAb
    cmp ah, 48h
    JE dirAr
    cmp ah, 1ch
    JE enter
    cmp ah, 3DH ;buscar
    JE f3
    cmp ah, 3CH
    je f2
    cmp ah, 3EH
    je f4
    cmp ah, 3FH
    JE limpiar
    mov byte ptr [ptrv], al
ENDM

LEERNUM MACRO funcion
    LIMPIABARRAS
    CURSOR 20, 1 ;posicionar en primera barra
    IMPCAD tletras
    LEERC tsize
    LEERC tsize+1 ;guardar  en  memoria
    call funcion
ENDM
; usa cx, si,  dl, ah, di
HEXDEC MACRO num, buffer
    ; Cargar el número hexadecimal en AX
    mov cx, 0
    lea si, buffer
    lea di, num
    xor ax, ax
    mov ax, [di]
    convertirDec:
        cmp al, 0 ;Si el cociente es ceri
        JE invertir
        inc cx ; repeticiones
        mov dl, 10
        div dl ;Dividir  ax  entre 10, cociente en al
        OR ah, 30h ;Convertir resto a digito 0-9
        mov byte ptr [si], ah ;mover  a buffer i.e 9176-$
        inc si
        XOR ah, ah
        jmp convertirDec
    
    invertir:
        invertirLoop:
            mov di, si ;apunta al caracter '6'
            dec di ; desfase
            lea si,  buffer
            mov al, [di] ;convervar  '6'
            mov ah, [si] ;conservar '9'
            mov byte ptr [di], ah ;mueve '9' a '6' 9179-$ | AL = '6'
            mov byte ptr [si], al ;mueve  AL  a '9'
            inc si
            dec di
        loop  invertirLoop
    ENDM

MOVCURSOR MACRO ptren, ptcol, salto
            local @sigren
            local @cont
            inc byte ptr [ptcol]
            cmp byte ptr [ptcol], 79
            JE @sigren
            cmp byte ptr [ptcol], 79
            JNZ @cont
            @sigren:
                    inc byte ptr [ptren]
                    mov byte ptr [ptcol], 1
                    jmp salto
            @cont:
ENDM

LIMPIARMEM MACRO ptrv, caracteres
    LEA DI, ptrv       ; Cargar la dirección del arreglo.
    MOV CX, caracteres           ; Número de bytes a limpiar.
    CLD
    MOV AL, 0            ; Valor 0 a llenar.
    REP STOSB            ; Limpiar el arreglo llenando con 0
ENDM

INTERRUMPIR MACRO ren
        CURSOR ren, 1
        IMPCAD tcontinuar
        mov ah, 1h             ; Leer un carácter
        int 21h 
ENDM

;LEE UNA PALABRA Y ALMACENA EN BUFFER
LEERPALABRA MACRO texto, buffer, caracteres
    local @leerini
    local @leerpalabra
    @leerini:
    LIMPIABARRAS
    CURSOR 20,1
    IMPCAD texto
    LIMPIARMEM buffer, 21
    mov cl, caracteres
    mov ch, 0
    LEA bx, buffer 
    @leerpalabra: ;repetir cx veces
        LEERC2 bx, @leerini
        INC bx
    loop @leerpalabra
    mov byte ptr [bx], '$';La palabra se leyo
ENDM

EDITORRESET MACRO
    CLS 2,1,19,78, 00011111b
    IMPRIMEBUFFER
    LEA si, tcuerpo ; Direccion al cuerpo de texto
    LEA di, ren ; Direccion a renglon  y columna
    mov byte ptr [di], 2 ;iniciar el columna 1, renglon 2
    mov byte ptr [di+1], 1
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
    tletras db "Caracteres en tu palabra: (01-20): $"
    tbuscar db "Palabra a buscar: $"
    treemplazar db "Palabra de reemplazo: $"
    terror db "Solo numeros de 01-20 $"
    tsize db 2 dup(0)
    tbuscando db 21 dup(0) ;Alojar  memoria
    treemplazando db 21 dup(0) ;Alojar  memoria
    tcantidad db "Cantidad: $"
    tdecimal db 5 dup (0), '$'
    treset db "Se llego al maximo de caracteres.$"
    tcontinuar db "Presione cualquier tecla para continuar al editor: $"
    rena db 0
    cola db 0
    renb db 0
    colb db 0 
    copia dw 0
    inicio dw 0
    num db 0
datos ends

codigo segment para 'code'
    UI PROC NEAR
        CLS 0,0,0,79, 01110000b ;Cabecera fondo
        CLS 2,1,19,78, 00011111b
        LIMPIABARRAS
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
    ;En renb, colb gaurdamos las direcciones  actuales
    BUSCAR PROC NEAR
        lea bx, num
        mov [bx], 0
        LEA bx, tsize
        cmp byte ptr [bx], '0'
        JE err1 ; si empieza en 0
        cmp byte ptr [bx], '0'
        JL buscaErr
        cmp byte ptr [bx], '2'
        JG buscaErr
        cmp byte ptr [bx], '2'
        JE err2 ; si empieza en 2
        cmp byte ptr [bx+1], '0'
        JL buscaErr
        cmp byte ptr [bx+1], '9'
        JG buscaErr

        buscarN:
        CADHEX bx, bx ;convertir cadena a número
        lea si, tsize
        LEERPALABRA tbuscar, tbuscando, [si]
        ;--Buscar palabra
        lea di, rena
        mov byte ptr [di+2], 2 ;renb
        mov byte ptr [di+3], 1
        lea bx, tcuerpo
        buscarPalabra:
            cmp byte ptr [bx], '$'
            JE buscaFin
            mov ch, byte ptr [di+2] ;ren
            mov cl, byte ptr [di+3];col actual
            mov byte ptr [di], ch ;mover a rena pos actual
            mov byte ptr [di+1], cl
            lea si, tbuscando ;palabra buscada
            checarPalabra:
                mov word ptr [di+4], bx
                mov dh, [bx]
                cmp byte ptr [si], '$' ;salir si se llego al final de la  palabra buscada
                je buscarPalabraCorrecto
                cmp byte ptr [si], dh;comparar letra de la  palabra con la  actual del buffer
                JNZ checarPalabraErr ;borrar si hay  error
                CLS2 [di+2],[di+3],[di+2],[di+3], 11101111b, di+4 ;resaltar caracter actual 
                inc bx
                inc si
                MOVCURSOR di+2, di+3, checarPalabra ;incrementar col
                jmp checarPalabra

        buscarPalabraCorrecto:
            ;si se descartara, di se recupera
            ;en si  va  el buffer
            lea si, num
            inc byte ptr [si] ;incrementar contador
            jmp buscarPalabra

        checarPalabraErr:
            mov word ptr [di+4], bx
            CLS2 [di], [di+1], [di+2],[di+3], 00011111b, di+4 ;si hay error, color original
            inc bx
            MOVCURSOR di+2, di+3, buscarPalabra ;incrementar col
            jmp buscarPalabra
        
        err1:
        cmp byte ptr [bx+1], '0';  si  da 00
        JLE buscaErr
        cmp byte ptr [bx+1], '9';  si  da MAS DE 9
        JG buscaErr
        jmp buscarN

        err2:
        cmp byte ptr [bx+1], '0'
        JNZ buscaErr
        jmp buscarN

        buscaErr:
        LIMPIABARRAS
        CURSOR 21, 1
        IMPCAD terror
        EDITORRESET
        jmp editor

        buscaFin:
        IMPRIMEBUFFER
        LIMPIABARRAS
        CURSOR 21, 1
        IMPCAD tcantidad
        HEXDEC num, tdecimal ;guardar contador  como cadena
        IMPCAD tdecimal
        INTERRUMPIR 20
        EDITORRESET
        LIMPIABARRAS
        jmp editor
    BUSCAR ENDP

    REEMPLAZAR PROC NEAR
        LEA bx, tsize
        cmp byte ptr [bx], '0'
        JL reempErr
        cmp byte ptr [bx], '2'
        JG reempErr
        cmp byte ptr [bx], '2'
        JE Rerr2 ; si empieza en 2
        cmp byte ptr [bx], '0'
        JE Rerr1 ; si empieza en 0
        cmp byte ptr [bx+1], '0' ;si empieza en  1
        JL reempErr
        cmp byte ptr [bx+1], '9'
        JG reempErr
        
        reemprN:
        CADHEX bx, bx ;Obtener  num de caracteres
        lea si, tsize ;num de  caracteres
        LEERPALABRA tbuscar, tbuscando, [si] ;almacena palabra  en tbuscando
        LEERPALABRA treemplazar, treemplazando, [si] ;almacena palabra  en treemplazando

        lea si, tbuscando ;palabra a  buscar
        lea bx, tcuerpo
        reemplazarLoop:
            cmp byte ptr [bx], '$'
            JE reempFin
            lea si, inicio
            mov [si], bx ;guardar inicio
            lea si, tbuscando ;palabra buscada
            reemplazarPalabra:
                mov dh, [bx]
                cmp byte ptr [si], '$' ;salir si se llego al final de la  palabra buscada
                je reemplazarCorrecto
                cmp byte ptr [si], dh;comparar letra de la  palabra con la  actual del buffer
                JNZ reemplazarPalabraErr ;borrar si hay  error
                inc bx
                inc si ;recorre el buffer bx  y  la palabra  buscada y compara
                jmp reemplazarPalabra

        reemplazarCorrecto:
            lea si, tsize ;num de  caracteres
            mov cl, [si]
            mov ch, 0
            lea si, inicio
            mov di, [si] ;mover inicio
            lea si, treemplazando
            cld
            rep movsb ;reemplazar de manera  ascendente
            jmp reemplazarLoop

        reemplazarPalabraErr:
            inc bx
            jmp reemplazarLoop
        
        Rerr2:
        cmp byte ptr [bx+1], '0'
        JNZ reempErr
        jmp reemprN

        Rerr1:
        cmp byte ptr [bx+1], '0';  si  da 00
        JLE reempErr
        cmp byte ptr [bx+1], '9';  si  da MAS DE 9
        JG reempErr
        jmp reemprN

        reempErr:
        LIMPIABARRAS
        CURSOR 21, 1
        IMPCAD terror
        EDITORRESET
        jmp editor

        reempFin:
        IMPRIMEBUFFER
        LIMPIABARRAS
        INTERRUMPIR 20
        EDITORRESET
        LIMPIABARRAS
        jmp editor
    REEMPLAZAR ENDP


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
        EDITORRESET
        editor:
            IMPCAR 20, 1, [si]
            cmp byte ptr [si], '$' ;Si se llego al final del cuerpo
            JE reset
            LEER [di], [di+1], si ;Renglon, columna, actualiza el cuerpo
            IMPCARB [di], [di+1], [si], 00011111b 
            inc si
            inc byte ptr [di+1] 
            LIMPIABARRAS
            cmp byte ptr [di+1], 79  ;Si se llega al final de la columna
            JE sigRen
            editorf:
            jmp editor

        sigRen:
        inc byte ptr [di] ;siguiente  renglon
        mov byte ptr [di+1], 1 ;inicar en 1
        jmp editorf
        
        reset:
        CURSOR 20, 1
        IMPCAD treset
        INTERRUMPIR 21
        LIMPIABARRAS
        dec si
        mov byte ptr [di+1], 78
        mov byte ptr [di],19 
        jmp editorf

        backspace:
            cmp byte ptr [di+1], 1 ;si se decremento en 1
            JE renAnterior
            backspaceLoop:
                cmp byte ptr [di+1], 1 ;si se llego  al inicio de renglon
                JE borrarCaracter
                dec byte ptr [di+1] ;caracter anterior
                dec si ;decrementa si
                backspaceC:
                    cmp byte ptr [si], 0
                    JNZ borrarCaracter
            jmp backspaceLoop
        
        renAnterior:
            cmp byte ptr [di], 2 ;ultima linea?
            je editor
            mov byte ptr [di+1], 78
            dec byte ptr [di]
            dec si
            jmp backspaceC
        
        borrarCaracter:
            mov byte ptr [si], 0
            CLS [di], [di+1], [di], [di+1], 00011111b ;borrar caracter
            jmp editorf

        enter:
            cmp byte ptr [di], 19 ; si es ultima linea no hacer nada
            JE editorf
            mov dl, 79 ;calcular bytes a recorrer
            sub dl, [di+1]
            mov ch,0
            mov cl, dl
            recorrerSI:
                inc si
            loop recorrerSI
            inc byte ptr [di]
            mov byte ptr [di+1],1
            jmp editorf
        
        dirAr:
            cmp byte ptr [di],2
            JE editorf ;primera linea
            mov cx, 0078
            recorrerSI2:
                dec si
            loop recorrerSI2
            dec byte ptr [di]
            jmp editorf
        
        dirAb:
            cmp byte ptr [di],19
            JE editorf ;ultima linea
            mov cx, 0078
            recorrerSI3:
                inc si
            loop recorrerSI3
            inc byte ptr [di]
            jmp editorf
            

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
        
        limpiar:
            LIMPIARMEM tcuerpo, 1404
            LIMPIABARRAS
            EDITORRESET
            jmp editor
        
        f2:
            EDITORRESET
            jmp editor
        
        f3:
            LEERNUM BUSCAR
            jmp editor

        f4:
            LEERNUM REEMPLAZAR
            jmp editor
        
        finMain:
        mov ah, 4Ch       ; Función DOS para terminar programa
        mov al, 0         ; Código de salida (0 significa sin errores)
        int 21h           ; Llamada a interrupció
    Main ENDP
codigo ends
    end Main