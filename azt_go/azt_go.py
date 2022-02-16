from typing import Optional

from fastapi import Body, HTTPException, APIRouter, Depends, Path, Query, status, Response
import core.service as service
from sqlalchemy import exc
from azt_go.schemas import LinksDetail, LinksBase, LinksDB, LinksList
from azt_go.models import Links, Categories
from azt_go.utils import gen_slug

router = APIRouter()


@router.post("/", response_model=LinksDetail, status_code=status.HTTP_201_CREATED, tags=['Links'])
async def link_generate(response: Response,
                        params: dict = Depends(service.default_parameters),
                        link: LinksBase = Body(..., ),
                        ):
    try:

        create = service.CreateMixin(db=params['db'], model=Links)

        if create.check_uniq(attribute='redirect_url', value=link.redirect_url):

            link = service.DetailMixin(query_value=["redirect_url", link.redirect_url],
                                       db=params['db'],
                                       model=Links).get_detail()

            response.status_code = status.HTTP_200_OK

            raise Exception(f"Link {link.redirect_url} is already created, id={link.id}")

        link = LinksDB(**link.dict(),
                       slug=gen_slug(link.name))

        link = create.create_object(item=link)

        return link

    except exc.IntegrityError:
        raise HTTPException(status_code=400, detail=f"Name {link.name} is already taken or category with id "
                                                    f"{link.category_id} does not exist")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{str(e)}")


# @router.get("/", response_model=LinksList, status_code=status.HTTP_200_OK, tags=['Links'])
# async def links_list(response: Response,
#                      params: dict = Depends(service.default_list_parameters),
#                      category_id:  Optional[int] = Query(None),
#                      category_name: Optional[str] = Query(None)):
#     try:
#         params = locals().copy()
#         params['search_fields'] = ['name', 'slug', 'redirect_url']
#
#         qr_codes = service.ListMixin(params=params, model=Links).get_list()
#
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"{str(e)}")


@router.get("/", response_model=LinksList, status_code=status.HTTP_200_OK, tags=['Links'])
async def links_list(response: Response,
                     params: dict = Depends(service.default_list_parameters),
                     category_id:  Optional[int] = Query(None),
                     category_name: Optional[str] = Query(None)):
    try:
        params = locals().copy()
        params['search_fields'] = ['name', 'slug', 'redirect_url']
        params['filter_fields'] = ['category_id', 'category_name']

        qr_codes = service.ListMixin(params=params, model=Links).get_list()

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{str(e)}")