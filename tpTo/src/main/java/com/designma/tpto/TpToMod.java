package com.designma.tpto;

import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.common.event.FMLPreInitializationEvent;
import net.minecraftforge.fml.common.event.FMLServerStartingEvent;
import net.minecraftforge.common.config.ConfigManager;
import net.minecraftforge.fml.client.event.ConfigChangedEvent;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;

@Mod(modid = TpToMod.MODID, useMetadata = true, name = TpToMod.NAME, version = TpToMod.VERSION)
public class TpToMod {
    public static final String MODID = "tpto";
    public static final String NAME = "TpTo";
    public static final String VERSION = "1.0.0";

    @Mod.EventHandler
    public void preInit(FMLPreInitializationEvent event) {
        // Initialize configuration
        ConfigManager.sync(MODID, net.minecraftforge.common.config.Config.Type.INSTANCE);
    }

    @Mod.EventHandler
    public void serverLoad(FMLServerStartingEvent event) {
        // Register the /tpto command
        event.registerServerCommand(new TpToCommand());
    }

    @Mod.EventBusSubscriber(modid = MODID)
    public static class ConfigHandler {
        @SubscribeEvent
        public static void onConfigChanged(ConfigChangedEvent.OnConfigChangedEvent event) {
            if (event.getModID().equals(MODID)) {
                // Sync the configuration when changes are made in-game
                ConfigManager.sync(MODID, net.minecraftforge.common.config.Config.Type.INSTANCE);
            }
        }
    }
}