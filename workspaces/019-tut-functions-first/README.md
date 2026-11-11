# 019 - Tutorial: Compose Strings With Functions

**Level:** Level 0 - HCL Foundations  
**Difficulty:** Easy  
**Points:** 67  
**Tags:** terraform, tutorial, functions, strings

## Scenario

Terraform's built-in functions transform values without hardcoding the result. Build a URL-friendly slug from an input, then format a versioned label from that slug.

## What to complete

- File: `main.tf`
- Task: Build the derived strings
- Create a lowercase, hyphenated slug and a formatted version label.

## Hints

**Why it matters:** Functions make derived values declarative. A slug built from the same input every time is easier to trust than a value someone copied into the file.

**What to do:** Compute two locals. The first should turn the input name into a lowercase string with spaces replaced by hyphens. The second should combine that slug with a version suffix using format().

**When to use it:** Use string functions when a value is composed from inputs and should update automatically. Avoid them when a plain literal is clearer.

**How to approach it:** Work inside out. First decide which function changes case, then which one replaces characters, then nest them. For the label, look at format() as a small template with placeholders and arguments.


## Constraints

- Use var.app_name as the source value.
- Build local.slug with lower() and replace().
- Build local.label with format().
- Export both values as outputs.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `app_name` | `string` | `My App` |

## Expected resources

- (see constraints)

## Expected outputs

- `slug`
- `label`

## How to test

```powershell
python judge.py test 19 --dir workspaces/019-tut-functions-first
```

> Hidden test details are only revealed after a submission.
