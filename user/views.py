# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product ,Category
from .serializers import ProductSerializer, ProductOwnerSerializer
from .serializers import CategoryWithProductsSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from math import ceil
from drf_spectacular.utils import(
    extend_schema,
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse
)



class ProductListView(APIView):
    def get(self, request):
        """
        Return a list of all products.
        """
        queryset = Product.objects.all()
        serializer_class = ProductSerializer
        products = Product.objects.all()
        print("products:::::::",products )
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)




class CategoryWithProductsListView(APIView):

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="category",
                type=str,
                description="filter by category.",
                enum=["all", "arayeshi", "behdashti"],
                required=False,
                default="behdashti",
            ),
            OpenApiParameter(
                name="search",
                type=str,
                description="Search for category names containing a specific letter or string.",
                required=False,
            ),
            OpenApiParameter(
                name="page",
                type=int,
                description="Page number.",
                required=True,
                default=1,
            ),
            OpenApiParameter(
                name="page_size",
                type=int,
                description="Number of items per page.",
                required=True,
                default=20,
            )
        ]
    )
    def get(self, request):
        """
        Return a list of categories with their associated products based on filtering and searching criteria.
        """
        category_name = request.query_params.get('category', 'behdashti')
        search_query = request.query_params.get('search', '')
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))

        # Filter categories based on the category_name
        if category_name and category_name != "all":
            categories = Category.objects.filter(name=category_name)
        else:
            categories = Category.objects.all()

        if not categories.exists():
            return Response({"message": f"No categories found with name '{category_name}'."},
                            status=status.HTTP_200_OK)

        # Get the category IDs for filtering products
        category_ids = categories.values_list('id', flat=True)

        # Filter products based on the category and search query
        if search_query:
            category_products = Product.objects.filter(category__in=category_ids, name__icontains=search_query)
        else:
            category_products = Product.objects.filter(category__in=category_ids)

        if not category_products.exists():
            return Response(
                {"message": f"No products found in category '{category_name}' with search query '{search_query}'."},
                status=status.HTTP_200_OK)

        # Paginate products
        total_products = category_products.count()
        total_pages = ceil(total_products / page_size)
        if page > total_pages:
            return Response({"message": f"Page {page} exceeds total number of pages ({total_pages})."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Apply pagination
        start = (page - 1) * page_size
        end = start + page_size
        paginated_products = category_products[start:end]

        # Get the product_owner from the first product (assuming all products belong to the same owner)
        product_owner = category_products.first().product_owner

        # Serialize the product_owner and products separately
        # product_owner_serializer = ProductOwnerSerializer(product_owner)
        products_serializer = ProductSerializer(paginated_products, many=True)

        # Combine both in the final response with pagination info
        return Response({
            # "product_owner": product_owner_serializer.data,
            "total_products": total_products,
            "total_pages": total_pages,
            "current_page": page,
            "page_size": page_size,
            "products": products_serializer.data,

        })




class SearchProductOwnerNameView(APIView):
    serializer_class = ProductSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="search",
                type=str,
                description="Search for products by owner's name.",
                required=True,
            ),
            OpenApiParameter(
                name="page",
                type=int,
                description="Page number.",
                required=False,
                default=1,
            ),
            OpenApiParameter(
                name="page_size",
                type=int,
                description="Number of items per page.",
                required=False,
                default=20,
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        # Retrieve search parameters from request
        owner_name = request.query_params.get('search', None)
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))

        # Filter products based on the owner's name
        queryset = Product.objects.filter(
            product_owner__name__icontains=owner_name) if owner_name else Product.objects.none()

        if not queryset.exists():
            return Response({"message": f"No products found for owner '{owner_name}'."}, status=status.HTTP_200_OK)

        # Pagination logic
        total_products = queryset.count()
        total_pages = ceil(total_products / page_size)

        if page > total_pages:
            return Response({"message": f"Page {page} exceeds total number of pages ({total_pages})."},
                            status=status.HTTP_400_BAD_REQUEST)

        start = (page - 1) * page_size
        end = start + page_size
        paginated_products = queryset[start:end]

        # Serialize the products
        serializer = self.serializer_class(paginated_products, many=True)

        return Response({
            "total_products": total_products,
            "total_pages": total_pages,
            "current_page": page,
            "page_size": page_size,
            "products": serializer.data
        }, status=status.HTTP_200_OK)



#