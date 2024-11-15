pila segment para stack 'stack'
    dw 32 dup(0)
pila ends

datos segment para 'data'
    three db 3
    momin db '11'
    alfmon db '???','$'
    montab  db 'JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'
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
        call c10conv ;convert to  binary
        call d10loc ;locate month
        call f10disp ;display  alpha month
        RET
    Main ENDP

    c10conv PROC NEAR
        mov  ah, momin
        mov al,momin+1
        xor ax,  3030h
        cmp ah, 0
        jz  c20
        sub ah, ah
        add al, 10
        c20: RET
    c10conv endp

    d10loc PROC NEAR
        lea si, montab
        dec  al
        mul three
        add si, ax
        mov cx,03
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
    
    