"""Richtext hooks."""
import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    InlineStyleElementHandler,
    BlockElementHandler,
)
from wagtail.core import hooks

@hooks.register("register_rich_text_features")
def register_centertext_inline_feature(features):
    """Creates centered text in our richtext editor and page."""

    # Step 1
    feature_name = "center_inline"
    type_ = "CENTERTEXTINLINE"
    tag = "span"

    # Step 2
    control = {
        "type": type_,
        "label": "Center Inline",
        "description": "Center Text, Compatible with block features",
        "style": {
            "display": "block",
            "text-align": "center",
        },
        'element': 'span',
    }

    # Step 3
    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    # Step 4
    db_conversion = {
        "from_database_format": {tag: InlineStyleElementHandler(type_)},
        "to_database_format": {
            "style_map": {
                type_: {
                    "element": tag,
                    "props": {
                        "class": "d-block text-center"
                    }
                }
            }
        }
    }

    # Step 5
    features.register_converter_rule("contentstate", feature_name, db_conversion)

    # Step 6, This is optional.
    features.default_features.append(feature_name)

@hooks.register("register_rich_text_features")
def register_centertext_block_feature(features):
    """Creates centered text in our richtext editor and page."""

    # Step 1
    feature_name = "center_block"
    type_ = "CENTERTEXT"
    tag = "p"

    # Step 2
    control = {
        "type": type_,
        "label": "Center Block",
        "description": "Center Text",
        "style": {
            "display": "block",
            "text-align": "center",
        },
        'element': tag,
    }

    # Step 3
    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.BlockFeature(control)
    )

    # Step 4
    db_conversion = {
        "from_database_format": {tag: BlockElementHandler(type_)},
        "to_database_format": {
            "block_map": {
                type_: {
                    "element": tag,
                    "props": {
                        "class": "text-center"
                    }
                }
            }
        }
    }

    # Step 5
    features.register_converter_rule("contentstate", feature_name, db_conversion)

    # Step 6, This is optional.
    features.default_features.append(feature_name)

