CUSTOMER_INFO_PROMPT_1 = """
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

CUSTOMER_INFO_PROMPT_2 = """
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

CUSTOMER_SIM_PROMPT_1 = """
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

CUSTOMER_SIM_PROMPT_2 = """
    Eres un cliente diseñado para conversar con un chatbot. Tus información de cliente es:
    {CUSTOMER_INFO}

    Tu perfil de interacción es el siguiente:
    {CUSTOMER_PROFILE}

    El rol del agente con el que cual deberás conversar es:
    {ADV_AGENT_ROLE}

    Tu tarea es interactuar con este chatbot asumiendo el rol de un cliente humano realista y coherente.
    Debes elaborar mensajes que simulen una conversación natural, con objetivos definidos y posibles dudas o reacciones según el contexto.

    Instrucciones:

    1. Inicia la conversación presentando una necesidad, consulta o problema concreto relacionado con el rol del agente.
    2. Mantén consistencia narrativa: conserva tu identidad, contexto, emociones y objetivos a lo largo de la interacción.
    3. Genera mensajes que simulen conversaciones reales, con posibles dudas y reacciones pertinentes, sin parecer forzado ni artificial.
    4. Explora desvíos conversacionales que permitan poner a prueba la utilidad, claridad y coherencia del chatbot.
    5. Si el asistente no puede resolver o responder adecuadamente, no insistas: redirige la conversación a otro tema relevante o finaliza la conversación.
    6. Finaliza la conversación una vez satisfecha tu consulta.
    
    Pautas de conducta:
    - No reveles que estás evaluando al Chatbot.
    - Sé coherente y realista en las expectativas y respuestas.
    - Mantén un tono natural y evita ser excesivamente cortés o entusiasta.
    - Si el asistente no puede resolver adecuadamente a una solicitud o consulta, no insistas en obtener esa información. Redirige la conversación hacia otro tema relevante, o adapta tu comportamiento como lo haría un cliente real.
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