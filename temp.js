T_(
  a_,
  { categoryTitle: (0, le.Z)("Window Appearance"), filter: this.props.filter },
  void 0,
  this.renderOpenInTabs(),
  this.renderShowUI(),
  this.renderUseNativeWindow(),
  !1,
  this.renderStatusBar(),
  this.renderToolbarCustomizations(),
  this.renderUserInterfaceZoom(),
  this.renderHUD()
),
(() => {
  const spacingDetails = [
    {
      key: "bookmarks",
      default: 24,
      label: "Bookmarks",
      // For identification
      mimeType: "vivaldi/x-bookmarks",
    },
    {
      key: "downloads",
      default: 52,
      label: "Downloads",
      // For identification
      settings: "DOWNLOADS_TREE",
    },
    {
      key: "history",
      default: 24,
      label: "History",
      settings: "HISTORY_PANEL",
    },
    {
      key: "notes",
      default: 24,
      label: "Notes",
      mimeType: "vivaldi/x-notes",
    },
    {
      key: "settingsNavigation",
      default: 28,
      label: "Settings Navigation",
      settings: "SETTINGS_TREE",
    },
    {
      key: "windowPanel",
      default: 24,
      label: "Window Panel",
      mimeType: "vivaldi/x-window-item",
    },
  ];
  const rowsHeight = 30;
  let items = [""];
  let section = [];
  // To avoid duplicates (menu editor)
  let usedKeys = [];

  spacingDetails.forEach((det) => {
    if (usedKeys.includes(det.key)) return;
    
    usedKeys.push(det.key);
    console.log(det.label)
    items.push(
      T_(
        "div",
        { className: "setting-single" },
        void 0,
        T_("h3", {}, void 0, det.label),
        T_("input", { type: "range", min: 12, max: 64, step: 1, value: rowsHeight }),
        T_("span", {}, void 0, rowsHeight[det.key] + "px")
      )
    );
    if (items.length >= 4) {
      console.log(items.length)
      section.push(T_("div", { className: "setting-group" }, ...items));
      console.log(section)
      items = [""];
    }
  });
  if (items.length) section.push(T_("div", { className: "setting-group" }, ...items));

  return T_(a_, { categoryTitle: "Tree Views Row Height", filter: this.props.filter, className: "setting-group unlimited" }, void 0, ...section);
})(),
T_(
  a_,
  { categoryTitle: (0, le.Z)("Custom UI Modifications"), filter: this.props.filter, className: "setting-group unlimited" },
  void 0,
  this.renderCustomStylingOptions()
),