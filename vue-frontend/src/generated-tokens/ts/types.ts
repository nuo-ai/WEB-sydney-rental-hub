/**
 * Do not edit directly
 * Generated on Mon, 06 Oct 2025 16:27:01 GMT
 */

export default tokens;

declare interface DesignToken {
  value: any;
  name?: string;
  comment?: string;
  themeable?: boolean;
  attributes?: {
    category?: string;
    type?: string;
    item?: string;
    subitem?: string;
    state?: string;
    [key: string]: any;
  };
  [key: string]: any;
}

declare const tokens: {
  "color": {
    "white": DesignToken,
    "black": DesignToken,
    "gray": {
      "50": DesignToken,
      "75": DesignToken,
      "100": DesignToken,
      "200": DesignToken,
      "300": DesignToken,
      "400": DesignToken,
      "500": DesignToken,
      "600": DesignToken,
      "700": DesignToken,
      "800": DesignToken,
      "900": DesignToken
    },
    "brand": {
      "primary": DesignToken,
      "hover": DesignToken,
      "active": DesignToken
    },
    "semantic": {
      "bg": {
        "primary": DesignToken,
        "secondary": DesignToken,
        "page": DesignToken
      },
      "text": {
        "primary": DesignToken,
        "secondary": DesignToken,
        "muted": DesignToken,
        "inverse": DesignToken
      },
      "border": {
        "default": DesignToken,
        "subtle": DesignToken
      }
    }
  },
  "font": {
    "size": {
      "xs": DesignToken,
      "sm": DesignToken,
      "md": DesignToken,
      "lg": DesignToken,
      "xl": DesignToken
    },
    "weight": {
      "regular": DesignToken,
      "medium": DesignToken,
      "semibold": DesignToken,
      "bold": DesignToken
    }
  },
  "space": {
    "xs": DesignToken,
    "sm": DesignToken,
    "md": DesignToken,
    "lg": DesignToken,
    "xl": DesignToken
  },
  "radius": {
    "sm": DesignToken,
    "md": DesignToken,
    "lg": DesignToken,
    "full": DesignToken
  },
  "shadow": {
    "sm": DesignToken,
    "md": DesignToken
  },
  "component": {
    "button": {
      "primary": {
        "bg": DesignToken,
        "color": DesignToken
      }
    }
  }
}
