def get_event_binding_key(organization: str, service: str):
    """
    acme.onboarding.1.event.user.created
      |       |      |        |      |-> Action (past verb)
      |       |      |        |-> domain entity
      |       |      |-> version
      |       |-> service
      |-> organization
    """
    return f"{organization}.{service}.*.event.#"
