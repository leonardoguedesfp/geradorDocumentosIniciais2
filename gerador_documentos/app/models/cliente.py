"""Dataclass representing a client with all required fields."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Cliente:
    nome_completo: str = ""
    nacionalidade: str = ""
    estado_civil: str = ""
    profissao: str = ""
    rg: str = ""
    cpf: str = ""
    logradouro_numero: str = ""
    complemento: str = ""
    bairro: str = ""
    cidade: str = ""
    uf: str = ""
    cep: str = ""
    email: str = ""
    telefone: str = ""
    parte_contraria: str = ""

    def endereco_completo(self) -> str:
        """Build full address string.

        Format: {Logradouro e Número}[, {Complemento}] — {Bairro}, {Cidade} ({UF}), CEP {CEP}
        Complemento is omitted if empty.
        """
        parts = [self.logradouro_numero.strip()]
        if self.complemento.strip():
            parts[0] += f", {self.complemento.strip()}"
        parts.append(f" — {self.bairro.strip()}, {self.cidade.strip()} ({self.uf.strip()}), CEP {self.cep.strip()}")
        return "".join(parts)

    def to_placeholder_dict(self) -> dict[str, str]:
        """Return a dict mapping placeholder names to their values."""
        from app.core.validators import normalize_name, normalize_cep

        nome = normalize_name(self.nome_completo.strip())
        cep = normalize_cep(self.cep.strip())

        return {
            "NOME_COMPLETO": nome,
            "NACIONALIDADE": self.nacionalidade.strip(),
            "ESTADO_CIVIL": self.estado_civil.strip(),
            "PROFISSAO": self.profissao.strip(),
            "RG": self.rg.strip(),
            "CPF": self.cpf.strip(),
            "ENDERECO_COMPLETO": self.endereco_completo(),
            "EMAIL": self.email.strip(),
            "TELEFONE": self.telefone.strip(),
            "PARTE_CONTRARIA": self.parte_contraria.strip(),
        }
