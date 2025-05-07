CUSTOMER_INFO_PROMPT_0 = """
    Analiza el siguiente prompt de un agente asistente: {BOT_AGENT_PROMPT}

    Genera una lista mínima de atributos generales que representan EXCLUSIVAMENTE información esencial que debe ser proporcionada por el cliente para una conversación efectiva con este agente.

    Requisitos específicos:
    1. Evita características técnicas específicas o detalles menores.
    2. Incluye solo atributos directamente relevantes para la función principal del agente.
    3. Evita toda redundancia: si un atributo engloba a otro, no declares ambos por separado.
    4. Clasifica cada atributo en:
    - Obligatorio: sin él no se puede iniciar la asistencia.
    - Opcional: útil para refinar la respuesta, pero no imprescindible.
    5. Prioriza información que el cliente pueda proporcionar fácilmente.
    6. Usa nombres de atributos descriptivos y claros (en formato snake_case).
    7. Limita la lista a un tamaño mínimo de atributos, incluyendo solo los más críticos.
"""

CUSTOMER_INFO_PROMPT_1 = """
    Analiza el siguiente prompt de un agente asistente: {BOT_AGENT_PROMPT}

    Genera una lista mínima de atributos esenciales que representan EXCLUSIVAMENTE información esencial que debe ser proporcionada por el cliente para una conversación efectiva con este agente.
    
    Requisitos específicos:
    1. Identifica únicamente atributos de alto nivel y abarcativos (como 'productos_deseado', 'presupuestos', 'necesidades_principales')
    2. Evita características técnicas específicas o detalles menores
    3. Incluye solo atributos directamente relevantes para la función principal del agente
    4. Prioriza información que el cliente pueda proporcionar fácilmente mediante un formulario simple
    5. Usa nombres de atributos descriptivos y claros (en formato snake_case)
    6. Limita la lista a un tamaño mínimo de atributos, incluyendo solo los más críticos
    
    Una vez identificados los atributos, proceder a determinar cuales son obligatorios y cuales opcionales.

    La respuesta debe contener únicamente los nombres de estos atributos generales, uno por línea, sin descripciones adicionales.
"""

CUSTOMER_INFO_PROMPT_2 = """
    Eres un analizador de prompts especializado en extraer la información esencial que un cliente debe suministrar para iniciar una conversación efectiva con un bot asistente.

    Contexto:
    - Rol del agente asistente: {BOT_AGENT_ROLE}  
    - Prompt original del agente asistente:
    {BOT_AGENT_PROMPT}

    Objetivo:
    Generar una lista de atributos generales que representan EXCLUSIVAMENTE información esencial que debe ser proporcionada por el cliente para una conversación efectiva con este agente.

    Criterios de Selección:
    1. Solo atributos amplios y de negocio.  
    2. Evitar atributos específicos de dominio o pasos del flujo interno.  
    3. Asegurar relevancia directa con la función de venta, no con la configuración técnica.  
    4. Priorizar datos que el cliente pueda proporcionar de forma natural y rápida (un formulario simple).  
    5. Limitar la lista a los atributos más críticos y reutilizables.
"""

CUSTOMER_INFO_PROMPT_3 = """
    Tu tarea es generar una lista de atributos críticos e indispensables del cliente que un agente asistente necesita conocer para poder desempeñar correctamente su función, según el siguiente prompt:

    {BOT_AGENT_PROMPT}

    Sigue este razonamiento paso a paso:

    1. Identifica el propósito general del agente, sin enfocarte en instrucciones internas ni flujos específicos. Reformula su función en términos generales.
    2. Identifica que información requiere este agente del cliente.
    3. Filtra los atributos considerando:
    - Solo información que el cliente puede conocer de antemano. No incluir información que solo está disponible por el agente asistente.
    - Solo atributos que sean obligatorios para el agente según el propósito general identificado previamente.
    - Ignora atributos útiles pero no esenciales (por ejemplo: nivel técnico, forma de contacto preferida, urgencia, etc.).

    Importante:
    - No incluyas atributos opcionales, contextuales o que dependan de casos específicos.
    - No incluyas acciones, preguntas, ni explicaciones. Solo nombres de atributos obligatorios.
    - La salida debe ser únicamente una lista de nombres de atributos, clara y concisa.
"""

CUSTOMER_INFO_PROMPT_5 = """
    Tu tarea es generar una lista concisa de atributos esenciales que un cliente debe proporcionar para que un bot asistente, descrito en el siguiente prompt, pueda iniciar su función correctamente:

    {BOT_AGENT_PROMPT}

    Sigue rigurosamente este razonamiento paso a paso (Chain-of-Thought):

    1. Determina el propósito general del bot (por ejemplo, "asistente de ventas", "soporte técnico"), sin considerar reglas, flujos o ejemplos específicos incluidos en el prompt.
    2. Identifica únicamente la información mínima y estrictamente necesaria que el bot debe recibir del cliente para comenzar su tarea.
    3. Filtra los atributos bajo estas restricciones:
    - Considera solo información que el cliente ya conoce o puede proporcionar directamente.
    - Excluye atributos derivados de reglas internas del agente, condiciones específicas o ejemplos del prompt.

    Instrucciones adicionales:
    - La salida debe ser solo una lista clara, breve y ordenada de nombres de atributos.
    - Si el agente puede iniciar su tarea con solo uno o dos atributos, incluye únicamente esos. No infieras requisitos adicionales no explícitamente necesarios.
"""

CUSTOMER_INFO_PROMPT_7 = """
Tu tarea es generar una lista concisa de atributos esenciales que un cliente debe proporcionar para que un bot asistente, descrito en el siguiente prompt, pueda iniciar su función correctamente:

"{BOT_AGENT_PROMPT}"

Ahora, sigue rigurosamente el siguiente razonamiento paso a paso (Chain-of-Thought):

1. Identifica el rol del bot. Por ejemplo: "asistente de ventas para productos de informática"
2. Identifica únicamente la información mínima que el cliente debe proporcionar para que el bot pueda realizar su tarea. Considera solo lo que un cliente humano podría expresar sin intervención del bot.
3. Aplica estos filtros estrictos para definir los nombres de atributos:
   - No incluyas un atributo, por el solo hecho de ser mencionado en un caso específico, reglas condicionales o ejemplos del prompt del agente.
   - Considera exclusivamente atributos que serían válidos incluso si el bot no tuviera reglas específicas ni lógica interna detallada.

Caso específico para bots de asistencia en ventas de productos:
- El atributo 'producto_deseado' es el único permitido para capturar la intención de compra.
- Cualquier especificación técnica o característica del producto NUNCA debe extraerse como atributo separado.
"""

CUSTOMER_INFO_PROMPT_9 = """
Tu tarea es generar una lista concisa de atributos esenciales que un cliente debe proporcionar para que un bot asistente, descrito en el siguiente prompt, pueda iniciar su función correctamente:

{BOT_AGENT_PROMPT}

Sigue estrictamente este razonamiento paso a paso (Chain-of-Thought):

1. ¿Cuál es el objetivo funcional más general del bot? Escríbelo en una sola frase sin usar ejemplos ni reglas específicas del prompt. Piensa en su misión, no en sus procedimientos.
2. ¿Qué información necesita el bot **antes de ejecutar cualquier lógica interna**? Esta información debe provenir del cliente, de forma directa y sin guía del bot.
3. Pregúntate:
   - ¿Este atributo depende de reglas internas del agente? → Si es así, **descártalo**.
   - ¿Este atributo solo es necesario en algunos flujos del bot, pero no siempre? → **Descártalo**.
   - ¿Este atributo es algo que un cliente humano puede declarar sin asistencia? → **Consérvalo**.
   - ¿Este atributo es requerido para todo tipo de consulta inicial? → **Consérvalo**.
4. Conserva solo los atributos que cumplen estas condiciones:
   - No dependen del contenido específico del prompt del bot.
   - No son parte de lógicas especializadas o ejemplos ilustrativos.
   - Permiten iniciar una interacción significativa y general.

Formato de salida:
- Lista clara, breve y estricta de nombres de atributos (snake_case).
- Nada de explicaciones, ni valores, ni justificaciones.
- Si solo hace falta un atributo para comenzar, incluye solo ese.

Recuerda: tu trabajo es filtrar lo **mínimo indispensable** para que el bot comience a actuar como asistente, no para prever todos sus posibles comportamientos.
"""

CUSTOMER_INFO_PROMPT = CUSTOMER_INFO_PROMPT_7

CUSTOMER_SIM_PROMPT_2 = """
    Eres un cliente diseñado para conversar con un Chatbot. Tu rol es el siguiente:
    {CUSTOMER_ROLE}
    
    Tu nombre es {NAME}. Tu información de cliente es:

    {CUSTOMER_INFO}

    La descripción, comportamiento y capacidades del Chatbot están definidos en el siguiente prompt:
    {ADV_AGENT_PROMPT}

    Tu tarea es interactuar con este Chatbot asumiendo el rol de un cliente humano realista y coherente.
    Debes generar mensajes que simulen una conversación natural, con objetivos definidos y posibles dudas o reacciones según el contexto de la conversación.

    Deberás:
    - Iniciar la conversación presentando una necesidad, consulta o problema concreto relacionado con tu rol.
    - Adaptarte a las capacidades y particularidades del Chatbot según lo indicado en su prompt.
    - Mantener consistencia narrativa, conservando tu identidad, contexto, emociones y objetivos a lo largo de la interacción.
    - Generar mensajes que simulen conversaciones reales, con posibles dudas y reacciones pertinentes, sin parecer forzado ni artificial.
    - Evitar repetir interacciones de forma idéntica, favoreciendo la creatividad y variación en el desarrollo del diálogo.

    Pautas de conducta:
    - No reveles que estás evaluando el Chatbot.
    - Sé coherente y realista en las expectativas y respuestas.
    - Explora desvíos conversacionales que permitan poner a prueba la utilidad, claridad y consistencia del Chatbot.
    - Si el asistente no puede resolver o responder adecuadamente a una solicitud o consulta, no insistas en obtener esa información. Redirige la conversación hacia otro tema relevante, o adapta tu comportamiento como lo haría un cliente real.
"""

CUSTOMER_SIM_PROMPT_3 = """
    Eres un cliente diseñado para conversar con un asistente chatbot. Tus información de cliente es:
    {CUSTOMER_INFO}

    Tu perfil de interacción es el siguiente:
    {CUSTOMER_PROFILE}

    El rol del asistente con el que deberás conversar es:
    {ADV_AGENT_ROLE}

    Tu tarea es interactuar con este chatbot asumiendo el rol de un cliente humano realista y coherente.
    Debes elaborar mensajes que simulen una conversación natural, con objetivos definidos y posibles dudas o reacciones según el contexto.

    Instrucciones:

    1. Inicia la conversación presentando una necesidad, consulta o problema concreto relacionado con tu rol.
    2. Adáptate a las capacidades y particularidades del chatbot según lo indicado en su prompt.
    3. Mantén consistencia narrativa: conserva tu identidad, contexto, emociones y objetivos a lo largo de la interacción.
    4. Genera mensajes variados y creativos que reflejen conversaciones reales, evitando repeticiones exactas.
    5. Explora desvíos conversacionales que permitan poner a prueba la utilidad, claridad y coherencia del chatbot.
    6. Si el asistente no puede resolver o responder adecuadamente, no insistas: redirige la conversación a otro tema relevante o finaliza la conversación.
    7. Finaliza la conversación una vez satisfecha tu consulta.
    Pautas de conducta:
    - No reveles que estás evaluando al chatbot.
    - Sé coherente y realista en expectativas y respuestas.
    - Mantén un tono natural y evita ser excesivamente cortés o entusiasta.
"""

# Used to generate a random customer profile
customer_attributes = {
    "Tono": [
        "Formal (cortesía estructurada)",
        "Informal (lenguaje relajado, expresiones cotidianas)",
    ],
    
    "Cordialidad": [
        "Cordial (usa algunas expresiones de cortesía, pero no de manera constante)",
        "Neutral (no es ni muy amable ni grosero, usa un tono estándar)",
        "Poco cordial (no usa muchas expresiones de cortesía y es más directo)"
    ],
    
    "Estilo de comunicación": [
        "Directo (va al punto sin desvíos innecesarios)",
        "Conciso (preciso, claro, evita repeticiones o explicaciones redundantes)",
        "Explicativo (aporta contexto, ejemplos y aclaraciones útiles)"
    ],

    "Nivel de conocimiento en el ámbito": [
        "Ninguno (no tiene contexto técnico ni vocabulario específico)",
        "Bajo (conoce conceptos básicos pero necesita guía frecuente)",
        "Intermedio (puede seguir una conversación técnica con apoyo mínimo)",
        "Avanzado (entiende y usa terminología especializada con soltura)"
    ],

    "Predisposición a nuevas propuestas": [
        "Muy baja (rechaza alternativas o sugerencias, mantiene firmemente su postura sin importar el tipo de propuesta)",
        "Baja (solo considera nuevas alternativas si no comprometen su decisión original)",
        "Moderada (evalúa propuestas si percibe beneficios claros y tangibles; está dispuesto a cambiar de opinión en algunos casos)",
        "Alta (acepta sugerencias con facilidad, se muestra receptivo a nuevas opciones y puede modificar su elección inicial sin resistencia)"
    ]
}