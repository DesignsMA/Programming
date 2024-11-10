pila segment para stack 'stack'
    dw 64 dup(0)
pila ends

datos segment para 'data'
    tmenu db "1. Suma#2. Resta#3. Multiplicacion#4. Division#5. Salir#Elige una opcion#: ", '$'
    tdato1 db "Dame dato 1 (0-9)#: ", '$'
    tdato2 db "Dame dato 2 (0-9)#: ", '$'
    tsuma db "La suma es : ", '$'
    tresta db "La resta es : ", '$'
    tmult db "La multiplicacion es : ", '$'
    tdiv db "Residuo: ", '$'
    tdiv2 db "#Cociente: ", '$'
    continuar db "##Presiona cualquier tecla para continuar: ",'$'
    d1 db 0
    d2 db 0
    renglon db 0
datos ends

codigo segment para 'code'
    CLS PROC NEAR
        mov ax, 0600h ; servicio 6 ; cero para limpiar toda la pantalla
        mov bh, 00000111b ; atributo  fondo negro letras grises
        mov cx, 0 ; recorrer desde renglon 0, columna 0
        mov dx, 184fh ; hasta 24, 79 toda la pantalla
        int 10h ; interrupcion de bios
        RET
    CLS ENDP

    IMPRIME PROC NEAR
        mov ah, 2 ; Necesita que SI contenga la cadena
        LEA bx, renglon
        mov [bx], 9
        dec si ; desfase

        saltolinea:
            mov bh, 0
            mov dl, 10
            mov dh, [bx] ; renglon
            int 10h ; Posicionar cursor
            ; BYTE PTR especifica el tamanio del contenido del apuntador
            inc byte ptr [bx]; siguiente renglon
            inc si; siguiente caracter
            jmp imprimir

        imprimir:
            mov dl, [si]
            cmp dl, '#'
            JE saltolinea
            cmp dl, '$'
            JE salir
            int 21h
            inc si
            jmp imprimir

        salir:
        RET
    IMPRIME ENDP

    LEER PROC NEAR
        call IMPRIME
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

    SUMA PROC NEAR
        call CLS
        LEA di, d1
        mov dx, [di]
        add dl, dh
        mov [di], dl
        LEA si, tsuma
        call IMPRIME
        mov dl, [di]
        add dl, 30h
        int 21h
        RET
    SUMA ENDP

    RESTA PROC NEAR
        call CLS
        LEA di, d1
        mov dx, [di]
        sub dl, dh
        mov [di], dl
        LEA si, tresta
        call IMPRIME
        mov dl, [di]
        add dl, 30h
        int 21h
        RET
    RESTA ENDP

    RESULTADO PROC NEAR  
        loop1:
            mov dl, [di]
            add dl, 30h
            mov ah,2
            int 21h
            inc di
        loop loop1
        RET
    RESULTADO ENDP

    MULT PROC NEAR
        call CLS
        LEA di, d1
        LEA si, d2
        mov al, [di]
        mul byte ptr [si]
        mov [di], ah
        mov [si], al
        LEA si, tmult
        call IMPRIME
        mov cx, 2
        call RESULTADO
        RET
    MULT ENDP

    DIVI PROC NEAR
        call CLS
        LEA di, d1
        LEA si, d2
        mov ah, 0
        mov al, [di]
        div byte ptr [si]
        mov [di], ah
        mov [si], al
        LEA si, tdiv
        call IMPRIME
        mov dl, [di]
        add dl, 30h
        int 21h
        LEA si, tdiv2
        call IMPRIME
        LEA si, d2
        mov dl, [si]
        add dl, 30h
        int 21h
        RET
    DIVI ENDP

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
        
        menu:
            LEA si, tdato1
            LEA di, d1
            call LEER
            LEA si, tdato2
            LEA di, d2
            call LEER

            call CLS
            LEA si, tmenu
            call IMPRIME
            mov ah, 1 ; opcion en al
            int 21h
            

            cmp al, '1'
            JE sum
            cmp al, '2'
            JE res
            cmp al, '3'
            JE multi
            cmp al, '4'
            JE divis
            cmp al, '5'
            JE fin
            
            jmp menu

        sum:
            call SUMA
            jmp siguiente	
        
        res:
            call RESTA
            jmp siguiente	
        
        multi:
            call MULT
            jmp siguiente	
        
        divis:
            call DIVI
            jmp siguiente
        
        siguiente:
            LEA si, continuar
            call IMPRIME
            mov ah, 1 ; opcion en al
            int 21h
            call CLS
            jmp menu

        fin:
            RET
    Main ENDP
codigo ends
    end Main
    
    