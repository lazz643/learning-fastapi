from fastapi import Depends, HTTPException, status
from strawberry.fastapi import GraphQLRouter
from app.graphql_schema import schema
from app.auth import get_current_user

# Create the GraphQL router
graphql_app = GraphQLRouter(schema)

# Create a protected GraphQL router that requires authentication
async def get_context(request):
    """Get context for GraphQL operations requiring authentication"""
    try:
        # Get token from Authorization header
        authorization = request.headers.get("Authorization")
        if authorization and authorization.startswith("Bearer "):
            token = authorization.replace("Bearer ", "")
            user = await get_current_user(token)
            return {"user": user}
        raise HTTPException(status_code=401)
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

protected_graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context
) 