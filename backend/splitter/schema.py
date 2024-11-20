from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter

group_id_parameter = OpenApiParameter(
    name="group_id",
    type=int,
    location=OpenApiParameter.QUERY,
    description="ID of the group to filter expenses",
)
simple_mode_parameter = OpenApiParameter(
    name="simple_mode",
    type=OpenApiTypes.BOOL,
    location=OpenApiParameter.QUERY,
    description="Flag indicating whether to use simple mode",
)

payer_id_parameter = OpenApiParameter(
    name="payer_id",
    type=OpenApiTypes.INT,
    location=OpenApiParameter.QUERY,
    description="ID of the payer",
)
