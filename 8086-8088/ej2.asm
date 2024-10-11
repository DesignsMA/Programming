pila segment para stack 'stack'
    dw 64 dup(0)
pila ends

datos segment para 'data'
    org 200H ;Iniciar en celda 200
    DB 61h, 62h, 63h, 64h, 65h, 31h, 32h, 33h ;Guardar valores a partir de 0200

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
        
        mov si, 200h
        mov di, 210h
        mov ax, [si] ; AH | 62h  AL | 61h
        sub ax, 2020h
        mov [di], ax ; 0210h | 41 0211h 42
        mov si, 202h
        mov di, 212h
        mov ax, [si] 
        sub ax, 2020h
        mov [di], ax
        mov si, 204h
        mov di, 214h
        mov ax, [si] 
        sub ax, 0020h
        mov [di], ax
        mov si, 206h
        mov di, 216h
        mov ax, [si] 
        mov [di], ax

        RET
    Main ENDP
codigo ends
    end Main
    
    