;; ======================================================
;; ===     R O B O T    R E C O G E    C A J A S     ====
;; ======================================================

(defglobal ?*nod-gen* = 0)

(deffacts juego	
)

(defrule derecha
	?f <- (dynamic robot ?x ?y $?a movimiento ?mov nivel ?niv prev ?)
	(tamanyo ?sizex ?sizey)
	(profundidad-maxima ?prof)
	(test (< ?niv ?prof))
	(test (not (member$ (create$ enemigo  (+ ?x 1) ?y) $?a)))
	(not (hueco =(+ ?x 1) ?y))
	(test (< ?x ?sizex))
	(test (neq ?mov izquierda))
	=>
	(assert (dynamic robot (+ ?x 1) ?y $?a movimiento derecha nivel =(+ ?niv 1) prev ?f))
  	(bind ?*nod-gen* (+ ?*nod-gen* 1))
	;;(printout t "Derecha (" ?x ", " ?y ") -> (" (+ ?x 1) ", " ?y ")" crlf)
)

(defrule izquierda
	?f <- (dynamic robot ?x ?y $?a movimiento ?mov nivel ?niv prev ?)
	(profundidad-maxima ?prof)
	(test (< ?niv ?prof))
	(test (not (member$ (create$ enemigo  (- ?x 1) ?y) $?a)))
	(not (hueco =(- ?x 1) ?y))
	(test (> ?x 1))
	(test (neq ?mov derecha))
	=>
	(assert (dynamic robot (- ?x 1) ?y $?a movimiento izquierda nivel =(+ ?niv 1) prev ?f))
  	(bind ?*nod-gen* (+ ?*nod-gen* 1))
	;;(printout t "Izquierda (" ?x ", " ?y ") -> (" (- ?x 1) ", " ?y ")" crlf)
)

(defrule arriba
	?f <- (dynamic robot ?x ?y $?a movimiento ?mov nivel ?niv prev ?)
	(profundidad-maxima ?prof)
	(test (< ?niv ?prof))
	(escalera ?x ?y)
	(tamanyo ?sizex ?sizey)
	(test (< ?y ?sizey))
	(test (neq ?mov abajo))
	=>
	(assert (dynamic robot ?x (+ ?y 1) $?a movimiento arriba nivel =(+ ?niv 1) prev ?f))
  	(bind ?*nod-gen* (+ ?*nod-gen* 1))
	;;(printout t "Arriba (" ?x ", " ?y ") -> (" ?x ", " (+ ?y 1) ")" crlf)
)

(defrule abajo
	?f <- (dynamic robot ?x ?y $?a movimiento ?mov nivel ?niv prev ?)
	(profundidad-maxima ?prof)
	(test (< ?niv ?prof))
	(escalera ?x =(- ?y 1))
	(test (> ?y 1))
	(test (neq ?mov arriba))
	=>
	(assert (dynamic robot ?x (- ?y 1) $?a movimiento abajo nivel =(+ ?niv 1) prev ?f))
  	(bind ?*nod-gen* (+ ?*nod-gen* 1))
	;;(printout t "Abajo (" ?x ", " ?y ") -> (" ?x ", " (- ?y 1) ")" crlf)
)

(defrule recoger
    	(declare (salience 1))
	?f <- (dynamic robot ?x ?y $?a caja ?x ?y $?b movimiento ? nivel ?niv prev ?)
	(profundidad-maxima ?prof)
	(test (< ?niv ?prof))
	=>
  	(bind ?*nod-gen* (+ ?*nod-gen* 1))
	(assert (dynamic robot ?x ?y $?a $?b movimiento recoger nivel =(+ ?niv 1) prev ?f))
	;;(printout t "Recoger" crlf)
)

(defrule disparar_mover_derecha
	?f <- (dynamic robot ?x ?y ?m $?a enemigo =(+ ?x 1) ?y $?b movimiento ?mov nivel ?niv prev ?)
	(profundidad-maxima ?prof)
	(test (< ?niv ?prof))
	(test (> ?m 0))
	(tamanyo ?sizex ?sizey)
	(not (hueco =(+ ?x 1) ?y))
	(test (< ?x ?sizex))
	(test (neq ?mov izquierda))
	=>
	(assert (dynamic robot =(+ ?x 1) ?y =(- ?m 1) $?a $?b movimiento derecha nivel =(+ ?niv 1) prev ?f))
  	(bind ?*nod-gen* (+ ?*nod-gen* 1))
	;;(printout t "Disparar y derecha (" ?x ", " ?y ") -> (" (+ ?x 1) ", " ?y ") Municion: " (- ?m 1) crlf)
)

(defrule disparar_mover_izquierda
	?f <- (dynamic robot ?x ?y ?m $?a enemigo =(- ?x 1) ?y $?b movimiento ?mov nivel ?niv prev ?)
	(profundidad-maxima ?prof)
	(test (< ?niv ?prof))
	(test (> ?m 0))
	(not (hueco =(- ?x 1) ?y))
	(test (> ?x 1))
	(test (neq ?mov derecha))
	=>
	(assert (dynamic robot =(- ?x 1) ?y =(- ?m 1) $?a $?b $?b movimiento izquierda nivel =(+ ?niv 1) prev ?f))
  	(bind ?*nod-gen* (+ ?*nod-gen* 1))
	;;(printout t "Disparar y izquierda (" ?x ", " ?y ") -> (" (- ?x 1) ", " ?y ") Municion: " (- ?m 1) crlf)
)



;; ==========================
;; ====   INICIO Y FIN   ====
;; ==========================


(defrule ganar
    	(declare (salience 2))
	(dynamic $?a nivel ?n $?)
	(test (not (member$ caja $?a)))
	=>
	(printout t "SOLUCION ENCONTRADA EN EL NIVEL " ?n crlf)
    	(printout t "NUMERO DE NODOS EXPANDIDOS O REGLAS DISPARADAS " ?*nod-gen* crlf)
	(halt)
)

(defrule perder
    	(declare (salience -1))
	=>
    	(printout t "SOLUCION NO ENCONTRADA" crlf)
    	(printout t "NUMERO DE NODOS EXPANDIDOS O REGLAS DISPARADAS " ?*nod-gen* crlf)
	(halt)
)

(deffunction inicio ()
        (reset)
	(printout t "Profundidad Maxima:= " )
	(bind ?prof (read))
	(printout t "Tipo de Busqueda " crlf "    1.- Anchura" crlf "    2.- Profundidad" crlf )
	(bind ?a (read))
	(if (= ?a 1)
	       then    (set-strategy breadth)
	       else   (set-strategy depth))
        (printout t " Ejecuta run para poner en marcha el programa " crlf)
	(assert (profundidad-maxima ?prof))
	
)

(deffunction camino
	(?f)
	(bind ?lista (fact-slot-value ?f implied)) ;;?lista <- hecho numero ?f
	(bind ?l2 (member$ nivel ?lista))          ;;?l2    <- indice de nivel en ?lista
	(bind ?n (nth (+ ?l2 1) ?lista))           ;;?n     <- nivel del hecho

	(bind ?dir (nth (length ?lista) ?lista))   ;;?dir   <- hecho anterior

	(bind ?mov (nth (- ?l2 1) ?lista))
	(bind ?path (create$ ?dir))
	;;(printout t ?dir "    " ?mov crlf)

	(loop-for-count (- ?n 1) 
		(bind ?lista (fact-slot-value (fact-index ?dir) implied))
		(bind ?dir (nth (length ?lista) ?lista))
		(bind ?l2 (member$ nivel ?lista))
		(bind ?mov (nth (- ?l2 1) ?lista))
		(bind ?path (create$ ?dir ?path)) 
	)

	?path
)