#ifndef __RESOURCE_gresource_H__
#define __RESOURCE_gresource_H__

#include <gio/gio.h>

G_GNUC_INTERNAL GResource *gresource_get_resource (void);

G_GNUC_INTERNAL void gresource_register_resource (void);
G_GNUC_INTERNAL void gresource_unregister_resource (void);

#endif
