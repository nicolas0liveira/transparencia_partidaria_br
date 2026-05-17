import os
from datetime import datetime
from pathlib import Path
from typing import Any, cast
from urllib.parse import urlparse

import pandas as pd
import requests

class CKANClient:
    def __init__(self, base_url: str, api_key: str | None = None, timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    def _headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = self.api_key
        return headers

    def _action(self, action: str, params: dict[str, Any]) -> dict[str, Any]:
        url = f"{self.base_url}/api/3/action/{action}"

        try:
            response = requests.get(
                url,
                params=params,
                headers=self._headers(),
                timeout=self.timeout,
            )
            response.raise_for_status()
        except requests.RequestException as e:
            raise RuntimeError(f"Erro HTTP ao acessar CKAN: {e}") from e

        data = response.json()

        if not data.get("success"):
            raise RuntimeError(f"Erro CKAN: {data}")

        return data["result"]
    

    #==================
    # HELPERS
    #==================
    def _get_filename_from_url(self, url: str) -> str:
        parsed = urlparse(url)
        return os.path.basename(parsed.path) or "downloaded_file"


    # ---------------------------
    # DATASETS
    # ---------------------------
    def package_list(self) -> list[str]:
        result = self._action("package_list", {})
        return cast(list[str], result)

    def package_show(self, name_or_id: str) -> dict[str, Any]:
        return self._action("package_show", {"name_or_id": name_or_id})

    def package_search(self, query: str, rows: int = 10, start: int = 0) -> dict[str, Any]:
        return self._action(
            "package_search",
            {
                "q": query,
                "rows": rows,
                "start": start,
            },
        )

    def list_resources(self, name_or_id: str) -> list[dict[str, Any]]:
        pkg = self.package_show(name_or_id)
        return pkg.get("resources", [])

    # ---------------------------
    # DATASTORE
    # ---------------------------
    def datastore_search(
        self,
        resource_id: str,
        limit: int = 100,
        filters: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {
            "resource_id": resource_id,
            "limit": limit,
        }
        if filters:
            params["filters"] = filters

        return self._action("datastore_search", params)

    def datastore_sql(self, sql: str) -> dict[str, Any]:
        return self._action("datastore_search_sql", {"sql": sql})

    # ---------------------------
    # PANDAS
    # ---------------------------
    def to_dataframe(self, resource_id: str, limit: int = 1000) -> pd.DataFrame:
        result = self.datastore_search(resource_id, limit=limit)
        return pd.DataFrame(result["records"])

    def sql_to_dataframe(self, sql: str) -> pd.DataFrame:
        result = self.datastore_sql(sql)
        return pd.DataFrame(result["records"])

    # ---------------------------
    # PARQUET
    # ---------------------------
    def to_parquet(
        self,
        resource_id: str,
        output_path: str,
        limit: int = 10000,
    ) -> str:
        df = self.to_dataframe(resource_id, limit=limit)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        df.to_parquet(output_path, engine="pyarrow", index=False)
        return output_path

    def incremental_to_parquet(
        self,
        resource_id: str,
        output_dir: str,
        chunk_size: int = 50000,
    ) -> list[str]:
        start = 0
        files: list[str] = []

        while True:
            result = self.datastore_search(resource_id, limit=chunk_size)
            records = result["records"]

            if not records:
                break

            df = pd.DataFrame(records)

            file_path = os.path.join(
                output_dir,
                f"part_{start}_{datetime.now():%Y%m%d_%H%M%S}.parquet",
            )

            os.makedirs(output_dir, exist_ok=True)
            df.to_parquet(file_path, engine="pyarrow", index=False)

            files.append(file_path)

            if len(records) < chunk_size:
                break

            start += chunk_size

        return files
    

    def download_resource(
        self,
        resource: dict,
        output_dir: str = "data/raw",
        filename: str | None = None,
        chunk_size: int = 8192,
    ) -> str:
        """
        Baixa um resource do CKAN via URL.

        Args:
            resource: dict do CKAN (resource)
            output_dir: diretório destino
            filename: nome customizado (opcional)
            chunk_size: tamanho do chunk para streaming

        Returns:
            caminho do arquivo salvo
        """

        url = resource.get("url")
        if not url:
            raise ValueError("Resource não possui URL")

        # nome do arquivo
        if filename:
            fname = filename
        else:
            fname = self._get_filename_from_url(url)

        output_path = Path(output_dir) / fname
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # download com streaming
        with requests.get(url, stream=True, timeout=30) as r:
            r.raise_for_status()

            with open(output_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)

        return str(output_path)