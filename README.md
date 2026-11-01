# Quote Batch

**Send the right numbers to the right client. Start with checked quotes.**

For freelancers, studios and small service teams preparing repeatable estimates. Generate editable quotation documents from approved scope, quantities and prices, with an auditable calculation for every amount.

![Website project quotation](examples/freelance-quotes/preview.png)

**Demo:** a website project and a support engagement for two fictional clients. [See the source data, expected totals and generated documents](examples/freelance-quotes/README.md).

## Try the example

Python 3.10+; **no third-party runtime packages or API keys** are needed.

```sh
git clone https://github.com/IFFiend/quote-batch.git
cd quote-batch
python3 scripts/quotes.py examples/freelance-quotes/input.json --out output/first-quotes
```

Open `output/first-quotes/index.html`. Each quote has editable HTML and calculation JSON. Windows can use `py` instead of `python3`.

## Prepare your own quotes

Copy [input.json](examples/freelance-quotes/input.json). Replace the issuer, client, scope, validity dates and approved terms. Enter quantities as decimal strings and unit prices as integer minor units: AUD 180.00 is `18000`. Supply a tax rate explicitly in basis points: 10% is `1000`, a known zero rate is `0`.

| Item | What happens |
| --- | --- |
| Fractional quantity | Calculated with decimal arithmetic |
| Supplied total | Cross-checked; disagreement blocks the whole batch |
| Multiple clients | Separate documents and identifiers |
| Small display | Line items scroll inside the page; totals stay visible |

The sample totals are **AUD 2,755.50** and **AUD 1,320.00**. [Calculation contract](references/calculation-contract.md) documents line-first rounding and supported currencies. Do not assume a default tax rate or another currency's decimal precision.

## Use as a skill

The root [SKILL.md](SKILL.md) is the agent entrypoint:

```sh
git clone https://github.com/IFFiend/quote-batch.git ~/.agents/skills/quote-batch
```

> Use $quote-batch to prepare these client estimates. Preserve the approved scope, use the supplied tax rates, independently recalculate totals and flag any disagreement. Keep the documents editable.

## What is checked

Decimal quantities, integer prices, explicit tax rates, dates, currency support, duplicate identifiers and supplied-total agreement. The output records line amounts, subtotal, tax, total and rounding policy.

This edition prepares **quotes**, not invoices or signed contracts. It does not choose a tax treatment, send documents, collect signatures or render PDF. Inspect scope, terms and client mapping before delivery. Experimental v0.1; no prompt-superiority claim.

Use the **Use report** issue form for calculation or workflow feedback; omit private customer details. Run `python3 -m unittest discover -s tests -v` for the local checks.

## License

[PolyForm Noncommercial 1.0.0](LICENSE).

## 中文

面向自由职业者、工作室和小型服务团队：从明细生成报价单，使用十进制计算并交叉检查总额。示例是网站项目和维护服务，输入与输出可逐项对照。当前只生成报价单，不自动发送或推断税率。使用权限以 LICENSE 为准。
