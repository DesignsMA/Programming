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

IMPCAR MACRO ren, col, car
    CURSOR ren, col
    mov dl, car
    int 21h
ENDM

LEER MACRO ptrv
    MOV AH, 01h      ; Función para leer un carácter desde el teclado
    INT 21h          ; Interrupción del DOS
    MOV byte ptr [ptrv], AL      ; Almacena el carácter leído en la variable `var`
ENDM

pila segment para stack 'stack'
    dw 32 dup(0)
pila ends

datos segment para 'data'
    three db 0Ah
    momin db '06'
    alfmon db '??????????','$'
    montab  db 'Enero     ','Febrero   ','Marzo     ','Abril     ','Mayo      ','Junio     ','Julio     ','Agosto    ','Septiembre','Octubre   ','Noviembre ','Diciembre '
    msg DB "Ingrese el mes (01-12): $"
    errorMsg DB "Error: solo se permiten numeros en un rango de 01 - 12.$"
    continuar db "Ingrese una tecla para continuar: $"
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
        inicio:
        CLS 0,0,23,80,00011111b
        CURSOR 2,2
        IMPCAD msg
        LEER momin ; primer caracter
        cmp byte ptr [momin], '0'
        JL err1 ;momin  es menor  que  cero
        cmp byte ptr [momin], '1'
        JG err1

        LEER momin+1 ;2do caracter
        cmp byte ptr [momin], '1'
        JE err2
        cmp byte ptr [momin+1], '1'
        JL err1
        cmp byte ptr [momin+1], '9'
        JG err1
        jmp noErr

        err1:
        CURSOR 2,2
        IMPCAD errorMsg
        mov byte ptr [momin], '0'
        mov byte ptr [momin+1], '1'
        jmp noErr

        err2:
        cmp byte ptr [momin+1], '0'
        JL err1
        cmp byte ptr [momin+1], '2'
        JG err1

        noErr:
        CURSOR 4,2
        call c10conv ;convert to  binary
        call d10loc ;locate month
        call f10disp ;display  alpha month
        CURSOR 6,2
        IMPCAD continuar
        LEER momin
        jmp inicio
        RET
    Main ENDP

    c10conv PROC NEAR
        mov  ah, momin
        mov al,momin+1 ;mover caracteres
        xor ax,  3030h ; realizar   xor (convierte a binario)
        cmp ah, 0 ;si es cero no seguir operando
        jz  c20
        sub ah, ah  ; eliminar ah
        add al, 10 ; si el número no es cero, sumar 10
        c20: RET
    c10conv endp

    d10loc PROC NEAR
        lea si, montab
        dec  al
        mul three
        add si, ax
        mov cx,0Ah
        cld
        lea di, alfmon
        rep movsb
        RET
    d10loc endp

    f10disp PROC NEAR
        lea  dx, alfmon
        mov  ah, 09
        int  21h
        RET
    f10disp endp
codigo ends
    end Main
    
    