.model large 
pila segment para stack 'stack'
    dw 64 dup(0)
pila ends

datos segment para 'data'
    tmenu db "Elige una opcion#: ", '$'
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
    tlista db "  [F2] Suma | [F3] Resta | [F4] Multiplicacion | [F5] Division | [ESC] Salir", '$'
    estilo1 db 01110000b
    estilo2 db 01110100b
datos ends


codigo segment para 'code'
    UI PROC NEAR
        mov dx, 0
        mov bh, 0
        mov ah,2
        int 10h
        mov ah, 9
        mov al, ' '
        LEA si, tlista
        LEA di, estilo1
        mov bl, [di]
        mov cx, 80
        int 10h

        ; Primer margen superior
        mov dh, 1           
        mov dl, 0         
        mov ah, 2           
        int 10h             

        mov dl, 218         
        int 21h             

        mov dl, 196         
        mov cx, 78          
        m1:
            int 21h         
            loop m1        

        mov dl, 191         
        int 21h             

        ; Lados izquierdo
        mov cx, 22          
        mov dh, 2           
        mov dl, 0           
        int 10h             

        lados1:
            mov dl, 179     
            int 21h         
            inc dh          
            mov dl, 0       
            int 10h        
            loop lados1    

        ; Lados derecho
        mov cx, 22          
        mov dh, 2           
        mov dl, 79          
        int 10h           

        lados2:
            mov dl, 179    
            int 21h         
            inc dh          
            mov dl, 79      
            int 10h        
            loop lados2     
        
        mov dh, 23
        mov dl, 0
        mov ah, 2
        int 10h

        mov dl, 192   
        int 21h             

        mov dl, 196         
        mov cx, 78          
        m2:
            int 21h         
            loop m2         

        mov dl, 217         
        int 21h           

        mov bh, 0
        mov dx,0
        mov ah,2
        int 10h ; Posicionar cursor
        cabecera:
            mov al, [si]
            cmp al, '$'
            JE cerrar
            mov ah, 9
            mov bh,0
            mov cx, 1
            cmp al, '['
            JE resaltado
            sigue:
            mov bl, [di]
            int 10h  ; imprimir
            inc dl
            inc si
            mov ah, 2
            int 10h ; Posicionar cursor
            cmp al, ']'
            JE normal
            JMP cabecera
        
        resaltado:
            LEA di, estilo2
            JMP  sigue
        normal:
            LEA di, estilo1
            JMP cabecera
        cerrar:
        RET
    UI ENDP

    CLS PROC NEAR
        mov ax, 0600h ; servicio 6 ; cero para limpiar toda la pantalla
        mov bh, 00011111b
        mov cx, 0201h ; recorrer desde renglon 1, columna 1
        mov dx, 164eh ; hasta 24, 78 toda la pantalla
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
    
    DATOSL PROC NEAR
            call CLS
            LEA si, tdato1
            LEA di, d1
            call LEER
            LEA si, tdato2
            LEA di, d2
            call LEER
    RET
    DATOSL ENDP
        
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
        menu:
            call CLS
            LEA si, tmenu
            call IMPRIME
            mov ah, 0 ; opcion en al
            int 16H
            
            cmp ah, 3CH
            JE sum
            cmp ah, 3DH
            JE res
            cmp ah, 3EH
            JE multi
            cmp ah, 3FH
            JE divis
            cmp ah, 01H
            JE fin
            
            jmp menu

        sum:
            call DATOSL
            call SUMA
            jmp siguiente	
        
        res:
            call DATOSL     
            call RESTA
            jmp siguiente	
        
        multi:   
            call DATOSL 
            call MULT
            jmp siguiente	
        
        divis:     
            call DATOSL 
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