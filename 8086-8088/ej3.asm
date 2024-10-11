pila segment para stack 'stack'
    dw 64 dup(0)
pila ends

datos segment para 'data'
    org 400H ;Iniciar en celda 400
    db 17h, 0EBh, 96h, 34h, 8Ah, 76h
    db 10 dup(0) ;Escribir cero en 10 celdas ( Para empezar en 410h, recordar que 10h es 16 en decimal
    db 59h, 42h, 3Dh, 98h, 17h, 43h ;A partir de 410h

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
        
        mov si, 400h ; En 8086 se asume que accedes a informacion en el segmento de datos
        mov bx, 410h
        mov di, 420h
        mov ax, [si] 
        mov cx, [bx]
        add ax, cx
        mov [di], ax
        mov si, 402h
        mov bx, 412h
        mov di, 422h
        mov ax, [si] 
        mov cx, [bx]
        add ax, cx
        mov [di], ax
        mov si, 404h
        mov bx, 414h
        mov di, 424h
        mov ax, [si] 
        mov cx, [bx]
        add ax, cx
        mov [di], ax
        RET
    Main ENDP
codigo ends
    end Main
    
    