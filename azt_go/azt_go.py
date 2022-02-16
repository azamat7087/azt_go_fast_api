from fastapi import Body, HTTPException, APIRouter, Depends, Path, Query, status, Response

import core.service as service
import azt_go.filters as filters

from sqlalchemy import exc
from azt_go.schemas import LinksDetail, LinksBase, LinksDB, LinksList, LinksPaginated, LinksUpdate, LinksUpdateSlug, \
    CategoriesPaginated, CategoriesDetail, CategoriesBase, CategoriesDB, CategoriesList, CategoryUpdateSlug
from azt_go.models import Links, Categories
from azt_go.utils import gen_slug
from auth.jwt_bearer import JWTBearer

router = APIRouter()

''' Links '''


@router.post("/links", response_model=LinksDetail, status_code=status.HTTP_201_CREATED, tags=['Links'],
             dependencies=[Depends(JWTBearer())])
async def link_generate(response: Response,
                        params: dict = Depends(service.default_parameters),
                        link: LinksBase = Body(..., )):
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


@router.get("/links", response_model=LinksPaginated, status_code=status.HTTP_200_OK, tags=['Links'],
            dependencies=[Depends(JWTBearer())])
async def links_list(response: Response,
                     params: dict = Depends(service.default_list_parameters),
                     filtering: dict = Depends(filters.link_filter)):
    try:
        params = locals().copy()

        params['search_fields'] = ['name', 'slug', 'redirect_url']

        links = service.ListMixin(params=params, model=Links).get_list()

        return links
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{str(e)}")


@router.get("/links/{slug}", response_model=LinksDetail, tags=['Links'])
async def links_detail(params: dict = Depends(service.default_parameters),
                       slug: str = Path(..., description="The slug of the link object",)):

    link = service.DetailMixin(query_value=["slug", slug], db=params['db'], model=Links).get_or_404()

    return link


@router.patch("/links/{pk}", response_model=LinksDetail, status_code=status.HTTP_200_OK, tags=['Links'],
              dependencies=[Depends(JWTBearer())])
async def link_update(params: dict = Depends(service.default_parameters),
                      pk: int = Path(..., description="The ID of the link object", gt=0),
                      link: LinksUpdate = Body(...,)):

    old_link = service.DetailMixin(query_value=["id", pk], db=params['db'], model=Links).get_or_404()

    name = link.name if link.name else old_link.name
    link = LinksUpdateSlug(**link.dict(),
                           slug=gen_slug(name))

    new_link = service.UpdateMixin(db=params['db'], model=Links).update(old_link, link)

    return new_link


@router.delete("/links/{pk}", status_code=status.HTTP_200_OK, tags=['Links'],
               dependencies=[Depends(JWTBearer())])
async def link_delete(params: dict = Depends(service.default_parameters),
                      pk: int = Path(..., description="The ID of the link object", gt=0),):

    service.DeleteMixin(db=params['db'], model=Links).delete_object(pk=pk)

    return {"delete": "success"}


''' Categories '''


@router.post("/categories", response_model=CategoriesDetail, status_code=status.HTTP_201_CREATED, tags=['Categories'],
             dependencies=[Depends(JWTBearer())])
async def create_category(response: Response,
                          params: dict = Depends(service.default_parameters),
                          category: CategoriesBase = Body(..., )):
    try:

        create = service.CreateMixin(db=params['db'], model=Categories)

        if create.check_uniq(attribute='name', value=category.name):

            category = service.DetailMixin(query_value=["name", category.name],
                                           db=params['db'],
                                           model=Categories).get_detail()

            response.status_code = status.HTTP_200_OK

            raise Exception(f"Category {category.name} is already created, id={category.id}")

        category = CategoriesDB(**category.dict(),
                                slug=gen_slug(category.name))

        category = create.create_object(item=category)
        return category
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{str(e)}")


@router.get("/categories", response_model=CategoriesPaginated, status_code=status.HTTP_200_OK, tags=['Categories'],
            dependencies=[Depends(JWTBearer())])
async def categories_list(response: Response,
                          params: dict = Depends(service.default_list_parameters),):
    try:
        params = locals().copy()

        params['search_fields'] = ['name', 'slug', 'description']

        categories = service.ListMixin(params=params, model=Categories).get_list()

        return categories
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{str(e)}")


@router.get("/categories/{slug}", response_model=CategoriesDetail, tags=['Categories'])
async def category_detail(params: dict = Depends(service.default_parameters),
                          slug: str = Path(..., description="The slug of the category object",)):

    category = service.DetailMixin(query_value=["slug", slug], db=params['db'], model=Categories).get_or_404()

    return category


@router.patch("/categories/{pk}", response_model=CategoriesDetail, status_code=status.HTTP_200_OK, tags=['Categories'],
              dependencies=[Depends(JWTBearer())])
async def link_update(params: dict = Depends(service.default_parameters),
                      pk: int = Path(..., description="The ID of the link object", gt=0),
                      category: CategoriesBase = Body(...,)):

    old_category = service.DetailMixin(query_value=["id", pk], db=params['db'], model=Categories).get_or_404()

    name = category.name if category.name else old_category.name

    category = CategoryUpdateSlug(**category.dict(),
                                  slug=gen_slug(name))

    new_category = service.UpdateMixin(db=params['db'], model=Links).update(old_category, category)

    return new_category


@router.delete("/category/{pk}", status_code=status.HTTP_200_OK, tags=['Categories'],
               dependencies=[Depends(JWTBearer())])
async def link_delete(params: dict = Depends(service.default_parameters),
                      pk: int = Path(..., description="The ID of the category object", gt=0),):

    service.DeleteMixin(db=params['db'], model=Categories).delete_object(pk=pk)

    return {"delete": "success"}
