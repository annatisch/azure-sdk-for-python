# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
from typing import Any, AsyncIterable, Callable, Dict, Generic, List, Optional, TypeVar
import warnings

from azure.core.async_paging import AsyncItemPaged, AsyncList
from azure.core.exceptions import HttpResponseError, ResourceExistsError, ResourceNotFoundError, map_error
from azure.core.pipeline import PipelineResponse
from azure.core.pipeline.transport import AsyncHttpResponse, HttpRequest

from ... import models

T = TypeVar('T')
ClsType = Optional[Callable[[PipelineResponse[HttpRequest, AsyncHttpResponse], T, Dict[str, Any]], Any]]

class DigitalTwinModelsOperations:
    """DigitalTwinModelsOperations async operations.

    You should not instantiate this class directly. Instead, you should create a Client instance that
    instantiates it for you and attaches it as an attribute.

    :ivar models: Alias to model classes used in this operation group.
    :type models: ~azure.digitaltwins.core.models
    :param client: Client for service requests.
    :param config: Configuration of service client.
    :param serializer: An object model serializer.
    :param deserializer: An object model deserializer.
    """

    models = models

    def __init__(self, client, config, serializer, deserializer) -> None:
        self._client = client
        self._serialize = serializer
        self._deserialize = deserializer
        self._config = config

    async def add(
        self,
        models: Optional[List[object]] = None,
        digital_twin_models_add_options: Optional["models.DigitalTwinModelsAddOptions"] = None,
        **kwargs
    ) -> List["models.DigitalTwinsModelData"]:
        """Uploads one or more models. When any error occurs, no models are uploaded.
        Status codes:


        * 201 Created
        * 400 Bad Request

          * DTDLParserError - The models provided are not valid DTDL.
          * InvalidArgument - The model id is invalid.
          * LimitExceeded - The maximum number of model ids allowed in 'dependenciesFor' has been
        reached.
          * ModelVersionNotSupported - The version of DTDL used is not supported.

        * 409 Conflict

          * ModelAlreadyExists - The model provided already exists.

        :param models: An array of models to add.
        :type models: list[object]
        :param digital_twin_models_add_options: Parameter group.
        :type digital_twin_models_add_options: ~azure.digitaltwins.core.models.DigitalTwinModelsAddOptions
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: list of DigitalTwinsModelData, or the result of cls(response)
        :rtype: list[~azure.digitaltwins.core.models.DigitalTwinsModelData]
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType[List["models.DigitalTwinsModelData"]]
        error_map = {404: ResourceNotFoundError, 409: ResourceExistsError}
        error_map.update(kwargs.pop('error_map', {}))
        
        _traceparent = None
        _tracestate = None
        if digital_twin_models_add_options is not None:
            _traceparent = digital_twin_models_add_options.traceparent
            _tracestate = digital_twin_models_add_options.tracestate
        api_version = "2020-10-31"
        content_type = kwargs.pop("content_type", "application/json")

        # Construct URL
        url = self.add.metadata['url']  # type: ignore

        # Construct parameters
        query_parameters = {}  # type: Dict[str, Any]
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}  # type: Dict[str, Any]
        if _traceparent is not None:
            header_parameters['traceparent'] = self._serialize.header("traceparent", _traceparent, 'str')
        if _tracestate is not None:
            header_parameters['tracestate'] = self._serialize.header("tracestate", _tracestate, 'str')
        header_parameters['Content-Type'] = self._serialize.header("content_type", content_type, 'str')
        header_parameters['Accept'] = 'application/json'

        body_content_kwargs = {}  # type: Dict[str, Any]
        if models is not None:
            body_content = self._serialize.body(models, '[object]')
        else:
            body_content = None
        body_content_kwargs['content'] = body_content
        request = self._client.post(url, query_parameters, header_parameters, **body_content_kwargs)

        pipeline_response = await self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [201]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize(models.ErrorResponse, response)
            raise HttpResponseError(response=response, model=error)

        deserialized = self._deserialize('[DigitalTwinsModelData]', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized
    add.metadata = {'url': '/models'}  # type: ignore

    def list(
        self,
        dependencies_for: Optional[List[str]] = None,
        include_model_definition: Optional[bool] = False,
        digital_twin_models_list_options: Optional["models.DigitalTwinModelsListOptions"] = None,
        **kwargs
    ) -> AsyncIterable["models.PagedDigitalTwinsModelDataCollection"]:
        """Retrieves model metadata and, optionally, model definitions.
        Status codes:


        * 200 OK
        * 400 Bad Request

          * InvalidArgument - The model id is invalid.
          * LimitExceeded - The maximum number of model ids allowed in 'dependenciesFor' has been
        reached.

        * 404 Not Found

          * ModelNotFound - The model was not found.

        :param dependencies_for: The set of the models which will have their dependencies retrieved. If
         omitted, all models are retrieved.
        :type dependencies_for: list[str]
        :param include_model_definition: When true the model definition will be returned as part of the
         result.
        :type include_model_definition: bool
        :param digital_twin_models_list_options: Parameter group.
        :type digital_twin_models_list_options: ~azure.digitaltwins.core.models.DigitalTwinModelsListOptions
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: An iterator like instance of either PagedDigitalTwinsModelDataCollection or the result of cls(response)
        :rtype: ~azure.core.async_paging.AsyncItemPaged[~azure.digitaltwins.core.models.PagedDigitalTwinsModelDataCollection]
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["models.PagedDigitalTwinsModelDataCollection"]
        error_map = {404: ResourceNotFoundError, 409: ResourceExistsError}
        error_map.update(kwargs.pop('error_map', {}))
        
        _traceparent = None
        _tracestate = None
        _max_items_per_page = None
        if digital_twin_models_list_options is not None:
            _traceparent = digital_twin_models_list_options.traceparent
            _tracestate = digital_twin_models_list_options.tracestate
            _max_items_per_page = digital_twin_models_list_options.max_items_per_page
        api_version = "2020-10-31"

        def prepare_request(next_link=None):
            # Construct headers
            header_parameters = {}  # type: Dict[str, Any]
            if _traceparent is not None:
                header_parameters['traceparent'] = self._serialize.header("traceparent", _traceparent, 'str')
            if _tracestate is not None:
                header_parameters['tracestate'] = self._serialize.header("tracestate", _tracestate, 'str')
            if _max_items_per_page is not None:
                header_parameters['max-items-per-page'] = self._serialize.header("max_items_per_page", _max_items_per_page, 'int')
            header_parameters['Accept'] = 'application/json'

            if not next_link:
                # Construct URL
                url = self.list.metadata['url']  # type: ignore
                # Construct parameters
                query_parameters = {}  # type: Dict[str, Any]
                if dependencies_for is not None:
                    query_parameters['dependenciesFor'] = self._serialize.query("dependencies_for", dependencies_for, '[str]', div=',')
                if include_model_definition is not None:
                    query_parameters['includeModelDefinition'] = self._serialize.query("include_model_definition", include_model_definition, 'bool')
                query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

                request = self._client.get(url, query_parameters, header_parameters)
            else:
                url = next_link
                query_parameters = {}  # type: Dict[str, Any]
                request = self._client.get(url, query_parameters, header_parameters)
            return request

        async def extract_data(pipeline_response):
            deserialized = self._deserialize('PagedDigitalTwinsModelDataCollection', pipeline_response)
            list_of_elem = deserialized.value
            if cls:
                list_of_elem = cls(list_of_elem)
            return deserialized.next_link or None, AsyncList(list_of_elem)

        async def get_next(next_link=None):
            request = prepare_request(next_link)

            pipeline_response = await self._client._pipeline.run(request, stream=False, **kwargs)
            response = pipeline_response.http_response

            if response.status_code not in [200]:
                error = self._deserialize(models.ErrorResponse, response)
                map_error(status_code=response.status_code, response=response, error_map=error_map)
                raise HttpResponseError(response=response, model=error)

            return pipeline_response

        return AsyncItemPaged(
            get_next, extract_data
        )
    list.metadata = {'url': '/models'}  # type: ignore

    async def get_by_id(
        self,
        id: str,
        include_model_definition: Optional[bool] = False,
        digital_twin_models_get_by_id_options: Optional["models.DigitalTwinModelsGetByIdOptions"] = None,
        **kwargs
    ) -> "models.DigitalTwinsModelData":
        """Retrieves model metadata and optionally the model definition.
        Status codes:


        * 200 OK
        * 400 Bad Request

          * InvalidArgument - The model id is invalid.
          * MissingArgument - The model id was not provided.

        * 404 Not Found

          * ModelNotFound - The model was not found.

        :param id: The id for the model. The id is globally unique and case sensitive.
        :type id: str
        :param include_model_definition: When true the model definition will be returned as part of the
         result.
        :type include_model_definition: bool
        :param digital_twin_models_get_by_id_options: Parameter group.
        :type digital_twin_models_get_by_id_options: ~azure.digitaltwins.core.models.DigitalTwinModelsGetByIdOptions
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: DigitalTwinsModelData, or the result of cls(response)
        :rtype: ~azure.digitaltwins.core.models.DigitalTwinsModelData
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["models.DigitalTwinsModelData"]
        error_map = {404: ResourceNotFoundError, 409: ResourceExistsError}
        error_map.update(kwargs.pop('error_map', {}))
        
        _traceparent = None
        _tracestate = None
        if digital_twin_models_get_by_id_options is not None:
            _traceparent = digital_twin_models_get_by_id_options.traceparent
            _tracestate = digital_twin_models_get_by_id_options.tracestate
        api_version = "2020-10-31"

        # Construct URL
        url = self.get_by_id.metadata['url']  # type: ignore
        path_format_arguments = {
            'id': self._serialize.url("id", id, 'str'),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}  # type: Dict[str, Any]
        if include_model_definition is not None:
            query_parameters['includeModelDefinition'] = self._serialize.query("include_model_definition", include_model_definition, 'bool')
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}  # type: Dict[str, Any]
        if _traceparent is not None:
            header_parameters['traceparent'] = self._serialize.header("traceparent", _traceparent, 'str')
        if _tracestate is not None:
            header_parameters['tracestate'] = self._serialize.header("tracestate", _tracestate, 'str')
        header_parameters['Accept'] = 'application/json'

        request = self._client.get(url, query_parameters, header_parameters)
        pipeline_response = await self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize(models.ErrorResponse, response)
            raise HttpResponseError(response=response, model=error)

        deserialized = self._deserialize('DigitalTwinsModelData', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized
    get_by_id.metadata = {'url': '/models/{id}'}  # type: ignore

    async def update(
        self,
        id: str,
        update_model: List[object],
        digital_twin_models_update_options: Optional["models.DigitalTwinModelsUpdateOptions"] = None,
        **kwargs
    ) -> None:
        """Updates the metadata for a model.
        Status codes:


        * 204 No Content
        * 400 Bad Request

          * InvalidArgument - The model id is invalid.
          * JsonPatchInvalid - The JSON Patch provided is invalid.
          * MissingArgument - The model id was not provided.

        * 404 Not Found

          * ModelNotFound - The model was not found.

        * 409 Conflict

          * ModelReferencesNotDecommissioned - The model refers to models that are not decommissioned.

        :param id: The id for the model. The id is globally unique and case sensitive.
        :type id: str
        :param update_model: An update specification described by JSON Patch. Only the decommissioned
         property can be replaced.
        :type update_model: list[object]
        :param digital_twin_models_update_options: Parameter group.
        :type digital_twin_models_update_options: ~azure.digitaltwins.core.models.DigitalTwinModelsUpdateOptions
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: None, or the result of cls(response)
        :rtype: None
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType[None]
        error_map = {404: ResourceNotFoundError, 409: ResourceExistsError}
        error_map.update(kwargs.pop('error_map', {}))
        
        _traceparent = None
        _tracestate = None
        if digital_twin_models_update_options is not None:
            _traceparent = digital_twin_models_update_options.traceparent
            _tracestate = digital_twin_models_update_options.tracestate
        api_version = "2020-10-31"
        content_type = kwargs.pop("content_type", "application/json-patch+json")

        # Construct URL
        url = self.update.metadata['url']  # type: ignore
        path_format_arguments = {
            'id': self._serialize.url("id", id, 'str'),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}  # type: Dict[str, Any]
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}  # type: Dict[str, Any]
        if _traceparent is not None:
            header_parameters['traceparent'] = self._serialize.header("traceparent", _traceparent, 'str')
        if _tracestate is not None:
            header_parameters['tracestate'] = self._serialize.header("tracestate", _tracestate, 'str')
        header_parameters['Content-Type'] = self._serialize.header("content_type", content_type, 'str')

        body_content_kwargs = {}  # type: Dict[str, Any]
        body_content = self._serialize.body(update_model, '[object]')
        body_content_kwargs['content'] = body_content
        request = self._client.patch(url, query_parameters, header_parameters, **body_content_kwargs)

        pipeline_response = await self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [204]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize(models.ErrorResponse, response)
            raise HttpResponseError(response=response, model=error)

        if cls:
            return cls(pipeline_response, None, {})

    update.metadata = {'url': '/models/{id}'}  # type: ignore

    async def delete(
        self,
        id: str,
        digital_twin_models_delete_options: Optional["models.DigitalTwinModelsDeleteOptions"] = None,
        **kwargs
    ) -> None:
        """Deletes a model. A model can only be deleted if no other models reference it.
        Status codes:


        * 204 No Content
        * 400 Bad Request

          * InvalidArgument - The model id is invalid.
          * MissingArgument - The model id was not provided.

        * 404 Not Found

          * ModelNotFound - The model was not found.

        * 409 Conflict

          * ModelReferencesNotDeleted - The model refers to models that are not deleted.

        :param id: The id for the model. The id is globally unique and case sensitive.
        :type id: str
        :param digital_twin_models_delete_options: Parameter group.
        :type digital_twin_models_delete_options: ~azure.digitaltwins.core.models.DigitalTwinModelsDeleteOptions
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: None, or the result of cls(response)
        :rtype: None
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType[None]
        error_map = {404: ResourceNotFoundError, 409: ResourceExistsError}
        error_map.update(kwargs.pop('error_map', {}))
        
        _traceparent = None
        _tracestate = None
        if digital_twin_models_delete_options is not None:
            _traceparent = digital_twin_models_delete_options.traceparent
            _tracestate = digital_twin_models_delete_options.tracestate
        api_version = "2020-10-31"

        # Construct URL
        url = self.delete.metadata['url']  # type: ignore
        path_format_arguments = {
            'id': self._serialize.url("id", id, 'str'),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}  # type: Dict[str, Any]
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}  # type: Dict[str, Any]
        if _traceparent is not None:
            header_parameters['traceparent'] = self._serialize.header("traceparent", _traceparent, 'str')
        if _tracestate is not None:
            header_parameters['tracestate'] = self._serialize.header("tracestate", _tracestate, 'str')

        request = self._client.delete(url, query_parameters, header_parameters)
        pipeline_response = await self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [204]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize(models.ErrorResponse, response)
            raise HttpResponseError(response=response, model=error)

        if cls:
            return cls(pipeline_response, None, {})

    delete.metadata = {'url': '/models/{id}'}  # type: ignore
