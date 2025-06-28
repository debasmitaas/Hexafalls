from fastapi import APIRouter
from app.api.native_products import create_product_and_auto_post_native

# Create a router that matches the frontend expectation
router = APIRouter(prefix="/native_products", tags=["native-products"])

# Re-expose the endpoint with the expected path
router.add_api_route(
    "/create-and-post-native",
    create_product_and_auto_post_native,
    methods=["POST"],
    response_model=dict
)
