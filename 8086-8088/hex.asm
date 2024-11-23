IMPCAD MACRO ptrv
    mov ah, 09h
    lea dx, ptrv
    int 21h
ENDM

CURSOR MACRO ren, col
    mov ah, 2
    mov bh, 0
    mov dh, ren
    mov dl, col
    int 10h
ENDM

pila segment para stack 'stack'
    dw 64 dup(0)
pila ends

datos segment para 'data'
    buffer db 5 dup(0), '$' ; Espacio para almacenar el número decimal (máximo 5 dígitos para 16 bits)
    res db "resultado$"
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
            ; Cargar el número hexadecimal en AX
    mov cx, 0
    lea si, buffer
    CURSOR  5,10
    IMPCAD res
    mov ax, 1000    ; Ejemplo: número hexadecimal a convertir (0x1A3F = 6719 en decimal)
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

    CURSOR 6,10
    IMPCAD buffer
    

        RET
    Main ENDP
codigo ends
    end Main
    
    